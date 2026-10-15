# RXP-Schritte so lesen, wie RXP sie einem Charakter zeigt, und prüfen, ob ein Neubau gespeicherte Stellen verschiebt.
#
# Aufruf:
#   python3 tools/rxp_schritte.py liste <Quelle> "<Guide-Name>" [--klasse druid] [--rasse tauren] [--von N] [--bis M] [--dungeons RFC,WC]
#   python3 tools/rxp_schritte.py vergleich <alte Quelle> <neue Quelle> "<Guide-Name>" --stelle N [--klasse ...] [--rasse ...]
#       Exit 1, wenn sich einer der Schritte 1..N in Zeilennummer, Kopf oder Inhalt ändert (dann fände RXP die Stelle nicht mehr).
#   --gruppe: nur Guides dieser Gruppe (Kombi_Guide.lua enthält jeden Guide-Namen zweimal: «Kombiguide (H)» zuerst, dann
#       «Kombiguide Dungeon (H)»). Ohne die Angabe gilt der erste Guide mit dem Namen.
#   --dungeons: eingeschaltete Dungeons (Kürzel wie in RXP, z. B. RFC,WC,BFD). Ohne die Angabe sind alle aus, wie in Forever:
#       RXP blendet dort die Dungeon-Auswahl aus und setzt sie beim Laden des gespeicherten Guides auf «keine»
#       (SettingsPanel.lua, RXPGuides.lua «TODO: Fix the dungeon selection for Camelot», v4.11.23).
# Quelle: eine Lua-Datei mit RXPGuides.RegisterGuide([[...]]), oder
#   git:REV:PFAD   aus diesem Repo, z. B. git:HEAD:addons/RXPGuides_KombiGuide/Kombi_Guide.lua
#   rxp:TAG:PFAD   aus dem RXP-Klon, z. B. rxp:v4.11.23:Guides/forever/Horde-12-22_Barrens.lua
#
# Nachgebaut nach RestedXP v4.11.23 (GuideLoader.lua ParseGuide/applies, RXPGuides.lua IsStepShown):
# - Kommentare: text:gsub("%-%-[^\r\n]*[\r\n]", "\n"); gezählt wird jede nicht leere Zeile, auch eine, die nur noch
#   Einrückung enthält. stepId = Zeilennummer + guideId (Adler-32 aus Gruppe und Name), die Nummer zählt nur gezeigte Schritte.
# - Gezeigt mit den Forever-Standard-Einstellungen: kein Hardcore (Forever erzwingt das), kein SSF, keine Dungeons
#   (ausser mit --dungeons), XP-Rate 1, Saison 0. #maxlevel und Stufen-Filter («<< 20») zählen nur mit --stufe.
# - Dungeons wie RXPs DungeonCheck (RXPGuides.lua): «.dungeon X» merkt sich X, «.dungeon !Y» merkt sich Y (je die letzte Zeile).
#   Gezeigt wird ein Schritt nicht, wenn Y an ist; sonst, wenn X an ist oder der Schritt kein X hat.
import argparse, os, re, subprocess, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


def load(src):
    if src.startswith("git:"):
        rev, path = src[4:].split(":", 1)
        return subprocess.run(["git", "-C", ROOT, "show", f"{rev}:{path}"], capture_output=True, text=True, check=True).stdout
    if src.startswith("rxp:"):
        tag, path = src[4:].split(":", 1)
        return subprocess.run(["git", "-C", os.path.join(ROOT, "vendor", "rxpguides"), "show", f"{tag}:{path}"],
                              capture_output=True, text=True, check=True).stdout
    return open(src, encoding="utf-8").read()


def applies(expr, me, level=None):
    """RXP-Filter hinter <<: / heisst oder, Leerzeichen und, ! nicht; eine Zahl heisst «ab Stufe» (ohne --stufe: erfüllt)."""
    expr = expr.strip().replace("(", "").replace(")", "")
    if not expr:
        return True
    for alt in expr.split("/"):
        ok = True
        for w in alt.split():
            neg = w.startswith("!")
            w2 = w.lstrip("!").lower()
            if re.fullmatch(r"\d+", w2):
                val = True if level is None else level >= int(w2)
            else:
                val = w2 in me
            if neg:
                val = not val
            if not val:
                ok = False
                break
        if ok:
            return True
    return False


def xprate_ok(v, rate=1.0):
    m = re.match(r"^([<>]?)\s*(\d+\.?\d*)-?(\d*\.?\d*)", v.strip())
    if not m:
        return True
    op, a1, a2 = m.groups()
    if op == "<":
        lo, hi = 0, float(a1) - 1e-4
    elif op == ">":
        lo, hi = float(a1) + 1e-4, 0xfff
    else:
        lo, hi = float(a1), (float(a2) if a2 else 0xfff)
    return lo <= rate <= hi


def dungeon_hidden(dg, dgskip, dungeons):
    """RXPGuides.lua addon.stepLogic.DungeonCheck: Grund fürs Ausblenden oder None."""
    if dgskip and dgskip in dungeons:
        return f"dungeon !{dgskip}"
    if dg and dg != dgskip and dg in dungeons:
        return None
    if not dg:
        return None
    return f"dungeon {dg}"


def steps(text, name, me, level=None, dungeons=frozenset(), group=None):
    blocks = re.findall(r"RXPGuides\.RegisterGuide\(\[\[(.*?)\]\]", text, re.S)
    block = next((b for b in blocks if re.search(r"^\s*#name\s+%s\s*$" % re.escape(name), b, re.M)
                  and (group is None or re.search(r"^\s*#group\s+%s\s*$" % re.escape(group), b, re.M))), None)
    if block is None:
        raise SystemExit(f"Guide «{name}»" + (f" in der Gruppe «{group}»" if group else "") + " nicht gefunden")
    block = re.sub(r"--[^\r\n]*[\r\n]", "\n", block)
    out, cur, skip, n = [], None, False, 0
    for seg in re.findall(r"[^\n\r]+", block):
        n += 1
        line = seg.strip()
        if line.startswith("step"):
            m = re.search(r"<<\s*(.+)", line)
            skip = bool(m) and not applies(m.group(1), me, level)
            if not skip:
                cur = {"line": n, "hdr": line, "body": [], "hide": [], "dg": None, "dgskip": None}
                out.append(cur)
            continue
        if skip or cur is None or not line:
            continue
        f = re.search(r"\s*<<\s*(.+)$", line)
        if f:                                   # RXP filtert jede Zeile, auch #-Tags (GuideLoader.lua parseLine)
            if not applies(f.group(1), me, level):
                continue
            line = line[:f.start()].rstrip()
        cur["body"].append(line)
        tag = line.split()[0].lower() if line.startswith("#") else ""
        arg = line[len(tag):].strip()
        if tag in ("#hardcore", "#ssf", "#som", "#hardcoreserver"):
            cur["hide"].append(tag)
        elif tag == "#xprate" and not xprate_ok(arg):
            cur["hide"].append(f"#xprate {arg}")
        elif tag == "#season" and "0" not in re.findall(r"\d+", arg):
            cur["hide"].append(f"#season {arg}")
        elif tag == "#maxlevel" and level is not None and arg.isdigit() and level > int(arg):
            cur["hide"].append(f"#maxlevel {arg}")
        elif re.match(r"^\.dungeon\s", line):
            inst = line.split(">>")[0].split()[1].upper()
            if inst.startswith("!"):
                cur["dgskip"] = inst[1:]       # «.dungeon !WC» heisst «überspringen, wenn WC an ist»
            else:
                cur["dg"] = inst
    for s in out:
        why = dungeon_hidden(s["dg"], s["dgskip"], dungeons)
        if why:
            s["hide"].append(why)
    shown = [s for s in out if not s["hide"]]
    for i, s in enumerate(shown, start=1):
        s["idx"] = i
    return shown


def main():
    ap = argparse.ArgumentParser(description="RXP-Schritte für einen Charakter lesen oder Stellen vergleichen")
    ap.add_argument("modus", choices=["liste", "vergleich"])
    ap.add_argument("quellen", nargs="+")
    ap.add_argument("--klasse", default="druid")
    ap.add_argument("--rasse", default="tauren")
    ap.add_argument("--stufe", type=int)
    ap.add_argument("--von", type=int, default=1)
    ap.add_argument("--bis", type=int)
    ap.add_argument("--stelle", type=int)
    ap.add_argument("--dungeons", default="", help="eingeschaltete Dungeons, z. B. RFC,WC,BFD (Standard: keine, wie in Forever)")
    ap.add_argument("--gruppe", help="nur Guides dieser Gruppe, z. B. «Kombiguide Dungeon (H)» (Standard: der erste Guide mit dem Namen)")
    a = ap.parse_args()
    me = {a.klasse.lower(), a.rasse.lower(), "horde", "forever", "dede"}   # Klasse, Rasse, Fraktion, Spiel, Sprache (applies)
    dg = frozenset(x.strip().upper() for x in a.dungeons.split(",") if x.strip())
    if a.modus == "liste":
        src, name = a.quellen
        for s in steps(load(src), name, me, a.stufe, dg, a.gruppe):
            if s["idx"] < a.von or (a.bis and s["idx"] > a.bis):
                continue
            keys = [b for b in s["body"] if re.match(r"^(#label|#completewith|\.accept|\.turnin|\.complete|\.collect|\.xp|\.train)\b", b)]
            print(f"#{s['idx']} Zeile {s['line']}: {s['hdr']} | " + " ; ".join(k[:70] for k in keys[:5]))
        return 0
    old, new, name = a.quellen
    if not a.stelle:
        raise SystemExit("vergleich braucht --stelle N (gespeicherte Schrittnummer des Testcharakters)")
    A, B = steps(load(old), name, me, a.stufe, dg, a.gruppe), steps(load(new), name, me, a.stufe, dg, a.gruppe)
    first, moved = None, []
    for x, y in zip(A, B):
        if (x["line"], x["hdr"], x["body"]) != (y["line"], y["hdr"], y["body"]):
            first = first or (x, y)
            if x["idx"] <= a.stelle and x["line"] != y["line"]:
                moved.append((x["idx"], x["line"], y["line"]))
    who = f"{name} ({a.rasse} {a.klasse})"
    if moved:
        i, l1, l2 = moved[0]
        print(f"PROBLEM {who}: Schritt #{i} verschiebt sich (Zeile {l1} -> {l2}), die Stelle #{a.stelle} fände RXP nicht mehr sicher")
        return 1
    if first:
        x, y = first
        note = "nur Inhalt geändert, Zeile gleich" if x["line"] == y["line"] else f"Zeile {x['line']} -> {y['line']}"
        print(f"OK {who}: erste Änderung bei #{x['idx']} ({note}), Stelle #{a.stelle} bleibt")
    else:
        print(f"OK {who}: Schritte 1..{min(len(A), len(B))} gleich")
    return 0


if __name__ == "__main__":
    sys.exit(main())
