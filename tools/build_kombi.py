# Kombi-Guide bauen: RXP-Route 1-22 (Horde, Forever) als eigene Gruppen, Berufsschritte aus der Plan-Tabelle einfügen, prüfen.
#
# Aufruf:  tools/fetch_rxp.sh v4.11.23 && python3 tools/build_kombi.py v4.11.23 [Ausgabeordner]
# Eingaben: data/kombi/plan.csv (eine Zeile pro Berufsschritt), data/karten/forever_karten.csv (Kartenecken), data/kombi/VERSION,
#           data/kombi/dungeons.csv (welche Dungeons in der Dungeon-Route an sind),
#           data/kombi/vorquests.csv (Dungeon-Vorquests als Zusatzschritte, nur in «Kombiguide (H)»; seit 0.6, Entscheid 16.10.)
# Ausgabe:  <Ausgabeordner, Standard build/>/RXPGuides_KombiGuide/{RXPGuides_KombiGuide.toc, Kombi_Guide.lua}
#
# Zwei Gruppen in einer Datei (eine Datei, damit beim Spieler /reload reicht):
#   «Kombiguide (H)»          RXPs Speedrun-Route, Schritte unverändert (gespeicherte Stellen der Testcharaktere bleiben);
#                             seit 0.6 dazu die Dungeon-Vorquests aus vorquests.csv als Zusatzschritte
#   «Kombiguide Dungeon (H)»  RXPs Dungeon-Route «(WIP) Dungeon Guide 1-22» (12-17, 17-22), Mulgore aus der Speedrun-Route
#                             (RXPs Dungeon-Mulgore bindet sie über #include ein). Die Dungeons aus dungeons.csv sind fest
#                             eingebaut: In Forever blendet RXP die Dungeon-Auswahl aus und setzt sie beim Laden auf «keine»
#                             (SettingsPanel.lua, RXPGuides.lua «TODO: Fix the dungeon selection for Camelot»; v4.11.23 und
#                             Hauptzweig 15.10.). Fest eingebaut heisst: Ein Schritt, den RXPs DungeonCheck mit dieser Auswahl
#                             ausblenden würde, fällt weg; bei den übrigen fallen die «.dungeon»-Zeilen weg.
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
MULGORE = "Guides/forever/Horde-1-12_Mulgore.lua"
GRUPPEN = [
    # gruppe, Quellen (Datei, nur diese Guides oder None = alle), Dungeons fest einbauen, #subgroup ersetzen,
    # Dungeon-Vorquests aus vorquests.csv einfügen (nur Speedrun: die Dungeon-Route führt RFC und WC schon selbst)
    {"gruppe": "Kombiguide (H)", "route": "Speedrun",
     "quellen": [(MULGORE, None), ("Guides/forever/Horde-12-22_Barrens.lua", None)],
     "dungeons": False, "subgroup": None, "vorquests": True},
    {"gruppe": "Kombiguide Dungeon (H)", "route": "Dungeon (WIP)",
     "quellen": [(MULGORE, None),
                 ("Guides/Forever/dungeon/Horde-12-22_Barrens.lua", ("12-17 The Barrens", "17-22 Stonetalon/Barrens/Ashenvale"))],
     "dungeons": True, "subgroup": "(WIP) Dungeon Guide 1-22", "vorquests": False},
]
LAST_NEXT = "RestedXP Forever Guide (H)\\22-24 Hillsbrad"   # nur, wenn RXPs #next keine Gruppe nennt (Speedrun-Route);
# nennt RXP eine Gruppe (Dungeon-Route: «RestedXP Horde 22-30\\22-24 Hillsbrad», v4.11.23 Zeile 3190), bleibt sein Ziel
# (Prüfbericht 15.10., A9; ob das Ziel im gekauften Guide existiert, ist ungeprüft: Test T5)
ZONES = {"1411": "Durotar", "1412": "Mulgore", "1413": "The Barrens", "1420": "Tirisfal Glades", "1421": "Silverpine Forest",
         "1440": "Ashenvale", "1454": "Orgrimmar", "1456": "Thunder Bluff", "1458": "Undercity"}
# Kontinent hinter der Karte in «.goto Karte/Kontinent,a,b» (RXP functions.lua: element.instance, 0 = Östliche Königreiche,
# 1 = Kalimdor). Östliche Königreiche laut Testlog KARTE «Kontinent 0» (15.10.) und wie in RXPs eigenen Schritten
# («.goto 1420/0,…», «1458/0,…», «1421/0,…», Horde-01-14_Undead.lua); alle anderen Karten im Plan liegen in Kalimdor.
OSTEN = {"1415", "1420", "1421", "1458"}


def read_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f, delimiter=";"))
    # Ein Semikolon im Text verschiebt die Spalten (DictReader legt den Rest unter None ab); dann stimmen «bis», «extra» und
    # «status» nicht mehr. Lieber abbrechen (16.10.: so wäre «#maxlevel» in der Spalte «dungeon» gelandet).
    bad = [r.get("nr") or str(i + 2) for i, r in enumerate(rows) if None in r or any(v is None for v in r.values())]
    if bad:
        raise SystemExit(f"{os.path.relpath(path, ROOT)}: falsche Spaltenzahl (Semikolon im Text?) in Zeile(n) " + ", ".join(bad))
    return rows


def show(path):
    return subprocess.run(["git", "-C", RXP, "show", f"{TAG}:{path}"], capture_output=True, text=True, check=True).stdout


def anchor_mode(anker):
    """'accept 96661 @softcore' -> ('accept 96661', 'softcore'): nur Schritte mit #softcore (bzw. #hardcore) zählen als
    Treffer. Nötig, wenn RXP denselben Schritt für beide Modi führt (6-12 Mulgore: Kaga Wildhoof)."""
    a, _, mode = anker.partition(" @")
    return a.strip(), mode.strip() or None


def anchor_regex(anker):
    """'accept 1656' -> Zeile '.accept 1656', 'label Name' -> '#label Name'."""
    cmd, _, arg = anchor_mode(anker)[0].partition(" ")
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
#   maxfertigkeit .maxskill id,menge             (z. B. Geselle gelernt: Maximum 150); bei 150 dazu .istrained <Zauber des Gesellen>
#                                                 (GESELLE unten), weil RXP .maxskill nur beim Aktivieren prüft
#   abgeben       .turnin id   ·   annehmen  .accept id
#   hingehen      nur .goto mit radius           (erledigt beim Ankommen)
#   hinweis       Text und +kurz                 (braucht «bis»; bleibt sichtbar, bis der Ziel-Schritt erledigt ist. Ohne das Kästchen
#                                                 wäre der Schritt nur Text, und RXP erledigt ihn sofort: GuideWindow.lua, UpdateStepCompletion)
#   manuell       +kurz                          (Kästchen zum Abhaken. «.itemcount» in extra prüft RXP nur, wenn der Schritt aktiv wird:
#                                                 fehlt das Material da schon, ist der Schritt erledigt; geht es mittendrin aus, Häkchen setzen)
#   gebiet        .zone id >>kurz                (id = Karten-ID; erledigt beim Betreten der Karte, functions.lua addon.functions.zone,
#                                                 wie RXPs Zeppelin-Schritt «.zone Tirisfal Glades», Horde-01-12_Durotar.lua; Häkchen = nicht hin)
# «bedingung» und «extra» nehmen mehrere rohe RXP-Zeilen, getrennt mit « // ».
# «radius» kommt roh hinter den Ort: «30» macht das Hingehen zur Bedingung, «0,0» macht das Ziel nachrangig (RXP lowPrio: der
# Pfeil zeigt erst dorthin, wenn kein anderes Ziel ansteht; so in RXPs Forever-Guides bei Schritten mit #completewith).
AKTIONEN = ("lernen", "kaufen", "ziel", "fertigkeit", "maxfertigkeit", "abgeben", "annehmen", "hingehen", "hinweis", "manuell",
            "gebiet")
# Geselle als Zauber (seit 0.5.3, Prüfbericht 16.10., C1): RXP v4.11.23 prüft «.maxskill» nur, wenn der Schritt aktiv wird
# (functions.lua: kein events.maxskill; GuideWindow.lua BindActiveStepElement ruft das Element einmal auf), ein Schritt hakt
# sich nach dem Lernen also nicht von selbst ab. «.istrained» hört auf TRAINER_SHOW, CHAT_MSG_SYSTEM, SKILL_LINES_CHANGED und
# TRAINER_UPDATE (events.istrained = events.train) und erledigt den Schritt, sobald der Zauber bekannt ist; Lehrer-Automatik
# hat es nicht (anders als «.train», das beim offenen Lehrerfenster selbst kauft, RXPGuides.lua OnTrainer).
# IDs: RXP DB/forever/db.lua, addon.professionID (meist Lehrling, Geselle, Experte …; bei Verzauberkunst steht 13920 vorne:
# 13920, 7411, 7412, 7413 …): Lederverarbeitung 2108, 3104; Verzauberkunst 7411, 7412; Kürschnerei 8613, 8617; Angeln
# 7620, 7731 (7620 beim Lernen im Testlog 13.10. gesehen); Kräuterkunde 2368 aus RXPs Guides/Herbalism.lua («.train 2368
# >> Train Journeyman Herbalism»). Kein RXP-Forever-Guide nutzt .istrained (Gegenprüfung 16.10.). Ob der Forever-Client
# den Gesellen unter diesen IDs führt, ist ungeprüft; das Testlog schreibt die ID beim Lernen (GELERNT). Kennt der Client
# die ID nicht, bleibt alles wie vorher (Häkchen setzen); kennt der Charakter sie schon vor dem Lernen, verschwände der
# Schritt zu früh (Test T29 prüft beides).
GESELLE = {"leatherworking": 3104, "enchanting": 7412, "skinning": 8617, "fishing": 7731, "herbalism": 2368}


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
        goto = f"    .goto {row['karte']}/{0 if row['karte'] in OSTEN else 1},{a:.2f},{b:.2f}"
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
        if row["menge"] == "150" and row["id"] in GESELLE:
            lines.append(f"    .istrained {GESELLE[row['id']]}")
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
    elif akt == "gebiet":
        if not (row["id"].isdigit() and kurz):
            raise SystemExit(f"Plan-Zeile {row['nr']}: «gebiet» braucht eine Karten-ID (id) und «kurz»")
        lines.append(f"    .zone {row['id']} >>{kurz}")
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


def dungeon_shown(dg, skip, on):
    """RXPGuides.lua addon.stepLogic.DungeonCheck mit der festen Auswahl «on»."""
    if skip and skip in on:
        return False
    if dg and dg != skip and dg in on:
        return True
    return not dg


def add_filter(header, g, where, problems):
    """Kopfzeile «step [<< F]» um die Bedingung g erweitern (Leerzeichen heisst und, GuideLoader.lua applies)."""
    m = re.match(r"^(\s*step)\s*(?:<<\s*(.*?))?\s*$", header)
    if not m or "--" in header:
        problems.append(f"{where}: Kopfzeile '{header.strip()}' unbekannt, Dungeon-Bedingung nicht einbaubar")
        return header
    old = (m.group(2) or "").strip()
    if not old:
        return f"{m.group(1)} << {g}"
    if "/" in old or "/" in g or "(" in old:
        problems.append(f"{where}: '{old}' und '{g}' lassen sich nicht einfach verbinden")
        return header
    return f"{m.group(1)} << {old} {g}"


def resolve_dungeons(steps, on, known, where, problems):
    """Dungeon-Auswahl fest einbauen: Schritte, die RXP mit «on» ausblenden würde, fallen weg; bei den übrigen die
    «.dungeon»-Zeilen. Eine «.dungeon»-Zeile mit eigenem Filter («<< Priest») gilt nur für diese Charaktere: Ist das
    Ergebnis für sie anders als für die übrigen, kommt die Bedingung in die Kopfzeile des Schritts."""
    out, dropped, filtered, tags = [], 0, 0, {}
    for st in steps:
        dl = []
        for k, l in enumerate(st):
            m = re.match(r"^\s*\.dungeon\s+(.*?)\s*$", l)
            if not m:
                continue
            rest, filt = m.group(1), None
            fm = re.search(r"\s*<<\s*(.+)$", rest)
            if fm:
                filt, rest = fm.group(1).strip(), rest[:fm.start()]
            if ">>" in rest or not rest.strip():
                problems.append(f"{where}: '.dungeon' mit Text oder ohne Dungeon wird nicht unterstützt: '{l.strip()}'")
                continue
            inst = rest.split()[0].upper()
            tags[inst.lstrip("!")] = tags.get(inst.lstrip("!"), 0) + 1
            if inst.lstrip("!") not in known:
                problems.append(f"{where}: Dungeon '{inst.lstrip('!')}' fehlt in data/kombi/dungeons.csv")
            dl.append((k, inst, filt))
        if not dl:
            out.append(st)
            continue
        filts = sorted({f for _, _, f in dl if f})
        if len(filts) > 1:
            problems.append(f"{where}: Schritt mit mehreren Dungeon-Filtern {filts} wird nicht unterstützt")
            out.append(st)
            continue

        def shown(fval):
            dg = skip = None
            for _, inst, f in dl:
                if f and not fval:
                    continue
                if inst.startswith("!"):
                    skip = inst[1:]
                else:
                    dg = inst
            return dungeon_shown(dg, skip, on)

        s1 = shown(True)
        s0 = shown(False) if filts else s1
        if not s1 and not s0:
            dropped += 1
            continue
        drop = {k for k, _, _ in dl}
        new = [l for k, l in enumerate(st) if k not in drop]
        if s1 != s0:
            f = filts[0]
            if not re.fullmatch(r"!?\w+", f):
                problems.append(f"{where}: Dungeon-Filter '{f}' lässt sich nicht umkehren")
            g = f if s1 else (f[1:] if f.startswith("!") else "!" + f)
            new[0] = add_filter(new[0], g, where, problems)
            filtered += 1
        if len(new) < 2:
            problems.append(f"{where}: Schritt ohne Inhalt nach dem Entfernen der Dungeon-Zeilen")
        out.append(new)
    return out, dropped, filtered, tags


plan = read_csv(os.path.join(ROOT, "data", "kombi", "plan.csv"))
maps = {m["karte"]: m for m in read_csv(os.path.join(ROOT, "data", "karten", "forever_karten.csv"))}
dungeon_rows = read_csv(os.path.join(ROOT, "data", "kombi", "dungeons.csv"))
DUNGEONS_KNOWN = {r["kuerzel"].strip().upper() for r in dungeon_rows}
DUNGEONS_ON = {r["kuerzel"].strip().upper() for r in dungeon_rows if r["an"].strip().lower() == "ja"}
for r in dungeon_rows:
    if r["an"].strip().lower() not in ("ja", "nein"):
        raise SystemExit(f"data/kombi/dungeons.csv: '{r['kuerzel']}' braucht an = ja oder nein")

# Dungeon-Vorquests (seit 0.6): gleiche Spalten wie plan.csv, dazu «dungeon»; nur in Gruppen mit «vorquests». Nummern mit
# «V» vorne, damit die Labels (KombiV1 …) nicht mit den Berufsschritten zusammenfallen.
VORQ = os.path.join(ROOT, "data", "kombi", "vorquests.csv")
vorquests = read_csv(VORQ) if os.path.exists(VORQ) else []
nrs = [r["nr"] for r in plan + vorquests]
if len(nrs) != len(set(nrs)):
    raise SystemExit("plan.csv und vorquests.csv: Nummer doppelt: " + ", ".join(sorted({n for n in nrs if nrs.count(n) > 1})))
# Zeilen mit Status «aus …» sind vorbereitet, aber nicht eingebaut (z. B. bis der Nutzer entscheidet, ob Schritte vor der
# gespeicherten Stelle eines Testcharakters dazukommen dürfen; offene Entscheidung 11)
aus = [r for r in plan + vorquests if (r.get("status") or "").strip().lower().startswith("aus")]
plan = [r for r in plan if r not in aus]
vorquests = [r for r in vorquests if r not in aus]


def make_blocks(rows):
    """Zeilen mit gleichem Guide, Anker und Position bilden einen Block (Reihenfolge wie in der Tabelle; Vorquests nach den
    Berufsschritten, z. B. der Abstecher nach Unterstadt nach der Berufssitzung in Orgrimmar)."""
    blocks = {}
    for row in rows:
        blocks.setdefault((row["guide"], row["anker"], row["position"]), []).append(row)
    return blocks

report, problems, out_blocks = [], [], []
dg_text = ", ".join(sorted(DUNGEONS_ON)) or "keine"
dg_off = ", ".join(sorted(DUNGEONS_KNOWN - DUNGEONS_ON)) or "keine"
for G in GRUPPEN:
    group = G["gruppe"]
    rows_g = plan + (vorquests if G["vorquests"] else [])
    blocks = make_blocks(rows_g)
    # Keine ungewollten Ketten (16.10.): Zeigt «#completewith» auf einen Schritt, der selbst «#completewith» hat, erledigt RXP
    # den ersten, sobald der zweite erledigt oder übersprungen ist (GuideWindow.lua UpdateStepCompletion: stepSkip des Ziels).
    # Zwei Annahmen hintereinander mit «bis next»: Nimmt man die zweite Quest an oder blendet «.xp …,1» sie aus, verschwände
    # die erste mit. Mehrere Annahmen am selben Ort zeigen darum auf ein Label danach (so der Abstecher: «KombiV17»). Ein Label
    # als Ziel ist erlaubt, wenn das Ende so gewollt ist (Plan-Zeile 9: Leder-Ziel bis zum Hinweis bei «Gathering Leather»).
    for rows in blocks.values():
        for r1, r2 in zip(rows, rows[1:]):
            if r1.get("bis") == "next" and r2.get("bis"):
                problems.append(f"{group}: Plan-Zeile {r1['nr']}: «bis next» trifft Zeile {r2['nr']} mit eigenem «bis» (Kette)")
    used, guide_labels, tags_all, group_blocks = set(), {}, {}, []
    for path, only in G["quellen"]:
        for body in re.findall(r"RXPGuides\.RegisterGuide\(\[\[(.*?)\]\]\)", show(path), re.S):
            head, steps = split_steps(body)
            name = next((re.sub(r"^\s*#name\s+", "", l).strip() for l in head if re.match(r"^\s*#name\s", l)), "?")
            if only and name not in only:
                continue
            where = f"{group} | {name}"
            newhead = []
            for l in head:
                if re.match(r"^\s*#group\s", l):
                    l = f"#group {group}"
                elif re.match(r"^\s*#subgroup\s", l) and G["subgroup"]:
                    l = f"#subgroup {G['subgroup']}"
                elif re.match(r"^\s*#(defaultfor|beta)\b", l):
                    continue
                elif re.match(r"^\s*#next\s+22-24 Hillsbrad\s*$", l):
                    l = f"#next {LAST_NEXT}"
                elif re.match(r"^\s*#next\s+[^;\n]*\\22-24 Hillsbrad\s*$", l):
                    report.append(f"{where}: #next bleibt wie bei RXP: {l.strip()[6:]}")
                newhead.append(l)
            if G["dungeons"]:
                steps, dropped, filtered, tags = resolve_dungeons(steps, DUNGEONS_ON, DUNGEONS_KNOWN, where, problems)
                for t, c in tags.items():
                    tags_all[t] = tags_all.get(t, 0) + c
                report.append(f"{where}: Dungeons fest eingebaut ({dg_text}): {dropped} RXP-Schritte entfallen, "
                              f"{filtered} mit Klassen-Bedingung")
            for (gname, anker, pos), rows in blocks.items():
                if gname != name:
                    continue
                rx, mode = anchor_regex(anker), anchor_mode(anker)[1]
                hits = [i for i, st in enumerate(steps) if any(re.search(rx, x) for x in st)
                        and (not mode or any(re.match(rf"^\s*#{mode}\b", x) for x in st))]
                if len(hits) != 1:
                    problems.append(f"{where}: Anker '{anker}' {len(hits)}x gefunden")
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
                    problems.append(f"{where}: Position '{pos}' unbekannt (vor/nach)")
                    continue
                new = [make_step(r, maps) for r in rows]
                steps[j:j] = new
                used.update(r["nr"] for r in rows)
                report.append(f"{where}: {len(new)} Schritte {pos} '{anker}' (RXP-Schritt {i + 1}) eingefügt, Zeilen {', '.join(r['nr'] for r in rows)}")
            report.append(f"{where}: {len(steps)} Schritte")
            block = "\n".join(newhead) + "\n" + "\n".join("\n".join(s) for s in steps)
            guide_labels[name] = set(re.findall(r"^\s*#label\s+(\S+)\s*$", block, re.M))
            group_blocks.append(block)
    if G["dungeons"] and tags_all:
        report.append(f"{group}: Dungeon-Zeilen in den Quellen: " + ", ".join(f"{t} {c}" for t, c in sorted(tags_all.items())))
    missing = [r["nr"] for r in rows_g if r["nr"] not in used]
    if missing:
        problems.append(f"{group}: nicht eingefügt: Plan-Zeilen " + ", ".join(missing))
    for row in rows_g:
        bis = row.get("bis") or ""
        if bis and bis != "next" and bis not in guide_labels.get(row["guide"], set()):
            problems.append(f"{group}: Plan-Zeile {row['nr']}: Label '{bis}' (bis) gibt es in '{row['guide']}' nicht")
    report.append(f"{group}: {len(group_blocks)} Guides, {len(used)} Plan-Zeilen eingefügt"
                  + (f" (davon {sum(1 for r in vorquests if r['nr'] in used)} Vorquests)" if G["vorquests"] else ""))
    out_blocks.extend((group, b) for b in group_blocks)

header = ("-- Kombi-Guide " + VERSION + " (WoW Forever, Horde): RXP-Route 1-22 mit Berufsschritten aus data/kombi/plan.csv\n"
          "-- Gruppe «Kombiguide (H)»: RXP-Speedrun-Route, dazu Dungeon-Vorquests als Zusatzschritte (data/kombi/vorquests.csv).\n"
          "-- Gruppe «Kombiguide Dungeon (H)»: RXP-Dungeon-Route (WIP), Mulgore aus der\n"
          "-- Speedrun-Route; Dungeons fest eingebaut (data/kombi/dungeons.csv): an " + dg_text + ", aus " + dg_off + "\n"
          "-- Basis RestedXP " + TAG + ", Quelle github.com/RestedXP/RXPGuides (CC BY-NC-SA 4.0), bearbeitet, gleiche Lizenz\n"
          "if not (RXPGuides and RXPGuides.RegisterGuide) then return end\n"
          "if UnitFactionGroup(\"player\") == \"Alliance\" then return end\n")
lua_src = header + "\n".join(f"RXPGuides.RegisterGuide([[\n{b}\n]])\n" for _, b in out_blocks)

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
unknown, seen = set(), set()
if len(cap) != len(out_blocks):
    problems.append(f"{len(cap)} Guides registriert, erwartet {len(out_blocks)}")
for i in range(1, len(cap) + 1):
    t = cap[i]
    group = out_blocks[i - 1][0] if i <= len(out_blocks) else "?"
    h = t.split("\nstep")[0]
    for need in ("#forever", "#name", "#group " + group, "<< Horde"):
        if need not in h:
            problems.append(f"Guide {i}: {need} fehlt im Kopf")
    for bad in ("#defaultfor", "#beta"):
        if re.search(r"^\s*" + bad + r"\b", h, re.M):
            problems.append(f"Guide {i}: {bad} noch da")
    m = re.search(r"^\s*#name\s+(.+?)\s*$", h, re.M)
    key = (group, m.group(1) if m else "?")
    if key in seen:
        problems.append(f"Guide {i}: Gruppe und Name doppelt: {key}")
    seen.add(key)
    if any(G["gruppe"] == group and G["dungeons"] for G in GRUPPEN) and re.search(r"^\s*\.dungeon\b", t, re.M):
        problems.append(f"Guide {i} ({group}): '.dungeon' noch da")
    for m in re.finditer(r"^\s*\.(\w+)", t, re.M):
        if m.group(1) not in funcs:
            unknown.add(m.group(1))
for row in plan + vorquests:
    for field in ("text", "kurz", "bedingung", "npc", "bis", "extra"):
        value = row.get(field) or ""
        if "--" in value:
            problems.append(f"Plan-Zeile {row['nr']}: '--' in {field}")
        if "[[" in value or "]]" in value:
            problems.append(f"Plan-Zeile {row['nr']}: '[[' oder ']]' in {field}")
    for value in (row.get("bedingung") or "").split(" // ") + (row.get("extra") or "").split(" // "):
        if re.search(r"^\s*\.\w+\s+[^>]*,,", value):
            problems.append(f"Plan-Zeile {row['nr']}: leeres Argument (',,') in '{value.strip()}': RXP überspringt es")
if unknown:
    problems.append("unbekannte Befehle: " + ", ".join(sorted(unknown)))
report.append(f"Lua 5.1 ok, {len(cap)} Guides registriert, Datei {len(lua_src) // 1024} KB")

d = os.path.join(OUT, "RXPGuides_KombiGuide")
os.makedirs(d, exist_ok=True)
open(os.path.join(d, "Kombi_Guide.lua"), "w", encoding="utf-8").write(lua_src)
open(os.path.join(d, "RXPGuides_KombiGuide.toc"), "w", encoding="utf-8").write(
    "## Interface: 16001\n## Title: RXP Guides Kombiguide\n"
    "## Notes: Kombi-Guide " + VERSION + ": RXP-Route 1-22 (Basis " + TAG + "), Speedrun mit Dungeon-Vorquests und Dungeon (WIP), mit Berufsschritten. CC BY-NC-SA 4.0\n"
    "## Author: ludes88\n## Version: " + VERSION + "-" + TAG + "\n## Dependencies: RXPGuides\n\nKombi_Guide.lua\n")
if aus:
    report.append("Vorbereitet, nicht eingebaut (Status «aus»): Plan-Zeilen " + ", ".join(r["nr"] for r in aus))
print("\n".join(report))
print("Probleme: " + ("; ".join(problems) if problems else "keine"))
sys.exit(1 if problems else 0)
