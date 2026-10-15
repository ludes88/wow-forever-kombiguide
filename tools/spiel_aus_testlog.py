# Spieldaten aus dem Testlog: Stufen pro Stunde, Zeit pro Gebiet, XP pro Gegner, Laufweg, Dungeon-Läufe.
#
# Aufruf:  python3 tools/spiel_aus_testlog.py <KombiTestlog.lua> [weitere Testlog-Dateien …]
#
# Liest die SavedVariables-Datei des Testlogs (eine oder mehrere; gleiche Zeilen zählen einmal):
#   Protokoll (alle Versionen)     Sitzungen (SITZUNG bis ENDE): Dauer, Stufe am Anfang und Ende («L16 68%» in jeder Zeile),
#                                  Quests mit XP (QUEST AB), Tode; Zeit und Stufen-Fortschritt pro Gebiet aus dem Abstand
#                                  zwischen zwei Zeilen (Lücken über 10 Minuten zählen als 10 Minuten, Wahl von Claude)
#   Testlog 3.7                    chars[Charakter].xp (XP pro Quelle), chars[Charakter].weg (Laufweg), dungeons (Läufe)
# Schreibt ins Repo nur Zahlen ohne Charakter- und Realmnamen und ohne Uhrzeiten (nur das Datum):
#   data/spiel/sitzungen.csv       eine Zeile pro Sitzung (ab 3 Minuten)
#   data/spiel/gebiete.csv         pro Sitzung, Gebiet und Stufe: Minuten, Stufen-Fortschritt, Quests, Tode (Protokoll)
#   data/spiel/xp_quellen.csv      pro Quelle, Kreatur, Gegnerstufe und eigener Stufe: Anzahl, XP, davon erholt (3.7)
#   data/spiel/laufweg.csv         pro Sitzung, Karte und Stufe: Minuten gesamt, in Bewegung, im Kampf, auf dem Flug, tot,
#                                  erholt (Gasthaus/Stadt), in Instanzen; Weg in Yards, XP, Kills (3.7)
# Der Bericht fasst gebiete.csv und laufweg.csv über alle Sitzungen zusammen. xp_quellen.csv hält die Summe über alle
# Charaktere (das Testlog zählt pro Charakter weiter; jeder Lauf ersetzt die Zeile mit dem neuen Stand).
#   data/spiel/dungeons.csv        eine Zeile pro Dungeon-Lauf (3.7)
#   docs/plan/spiel.md             Bericht
# Neue Zeilen kommen dazu, gleiche (gleicher Schlüssel) werden ersetzt; so wächst der Verlauf über mehrere Testlogs.
# Die Kennung einer Sitzung ist ein Prüfwert (SHA-256, 8 Zeichen) der SITZUNG-Zeile; der Name lässt sich daraus nicht lesen.
import csv, hashlib, io, math, os, re, sys
from collections import defaultdict
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ah_aus_testlog as at  # noqa: E402  (Lua-Datei lesen)

ROOT = at.ROOT
D = os.path.join(ROOT, "data", "spiel")
BERICHT = os.path.join(ROOT, "docs", "plan", "spiel.md")
KARTEN = os.path.join(ROOT, "data", "karten", "forever_karten.csv")
LUECKE = 600          # Sekunden: längere Abstände zwischen zwei Zeilen zählen nur so viel (Pause, Fenster offen)
MIN_SITZUNG = 180     # Sekunden: kürzere Sitzungen (/reload, Charakterwechsel) zählen nicht
WEG_LUECKE = 90       # Sekunden: Laufweg-Proben kommen spätestens alle 60 s; längere Abstände = Ausloggen oder Pause
ZEILE = re.compile(r"^(\d\d)\.(\d\d)\. (\d\d):(\d\d):(\d\d) \| ([^|]+?) \| (.*)$")
KONTEXT = re.compile(r"^L(\d+) (\d+)% \| ([^|]*) \| ([^|]*) \| RXP ([^|]*?)(?: \| (.*))?$")
F = {
    "sitzungen": ["kennung", "datum", "dauer_min", "stufe_von", "stufe_bis", "stufen_pro_h", "quests", "quest_xp", "tode",
                  "gebiete", "rxp_von", "rxp_bis", "kombiguide", "testlog"],
    "gebiete": ["kennung", "datum", "gebiet", "stufe", "minuten", "stufen", "quests", "quest_xp", "tode"],
    "xp_quellen": ["art", "kreatur", "gegnerstufe", "stufe", "anzahl", "xp", "xp_je", "anzahl_erholt", "xp_erholt",
                   "xp_je_ohne_erholt", "stand"],
    "laufweg": ["kennung", "datum", "karte", "name", "stufe", "minuten", "bewegung_min", "kampf_min", "flug_min", "tot_min",
                "erholt_min", "instanz_min", "yards", "xp", "kills"],
    "dungeons": ["kennung", "datum", "instanz", "name", "art", "dauer_min", "draussen_min", "wieder", "xp", "xp_pro_h", "kills",
                 "geld_kupfer", "beute", "stapel", "tode", "stufe_von", "stufe_bis", "gruppe", "ende", "testlog"],
}


def kennung(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:8]


def lade(pfade):
    """Protokollzeilen (ohne Doppelte, nach Zeit sortiert), dazu Laufweg, XP-Quellen und Dungeon-Läufe aller Dateien."""
    log, weg, xp_ch, dg = [], {}, defaultdict(lambda: defaultdict(lambda: defaultdict(int))), {}
    jahr = datetime.now().year
    for p in pfade:
        db = at._py(at._lua_tabelle(open(p, encoding="utf-8", errors="replace").read()))
        for s in (db.get("ahScans") or []):
            if str(s.get("datum", ""))[:4].isdigit():
                jahr = int(str(s["datum"])[:4])
        log += [str(z) for z in (db.get("log") or [])]
        for key, c in (db.get("chars") or {}).items():
            if not isinstance(c, dict):
                continue
            ch = kennung(str(key))
            for z in (c.get("weg") or []):
                weg.setdefault(ch, set()).add(str(z))
            for k, v in (c.get("xp") or {}).items():
                if isinstance(v, dict):
                    e = xp_ch[ch][str(k)]
                    for f in ("n", "xp", "nE", "xpE"):
                        e[f] = max(e[f], int(v.get(f) or 0))   # gleiche Daten in mehreren Dateien: nicht doppelt zählen
        for r in (db.get("dungeons") or []):
            if isinstance(r, dict):
                dg[kennung(f"{r.get('char')}|{r.get('start')}|{r.get('id')}")] = r
    xp = defaultdict(lambda: defaultdict(int))   # Summe über die Charaktere
    for per in xp_ch.values():
        for k, e in per.items():
            for f, v in e.items():
                xp[k][f] += v
    seen, uniq = set(), []
    for z in log:
        if z not in seen:
            seen.add(z)
            uniq.append(z)
    def zeit(z):
        m = ZEILE.match(z)
        return datetime(jahr, int(m.group(2)), int(m.group(1)), int(m.group(3)), int(m.group(4)), int(m.group(5))) if m else None
    uniq = [(zeit(z), z) for z in uniq]
    uniq = [(t, z) for t, z in uniq if t]
    uniq.sort(key=lambda tz: tz[0])
    return uniq, {k: sorted(v, key=lambda s: int(s.split()[1]) if s.startswith("S ") else int(s.split()[0])) for k, v in weg.items()}, xp, dg


def stufe(m):
    return int(m.group(1)) + int(m.group(2)) / 100


def sitzungen(log):
    """Sitzungen aus dem Protokoll: Liste von dicts mit den Zeilen (Zeit, Art, Kontext-Match, Text)."""
    out, cur = [], None
    for t, z in log:
        m = ZEILE.match(z)
        art, rest = m.group(6), m.group(7)
        k = KONTEXT.match(rest)
        if art == "SITZUNG":
            if cur:
                out.append(cur)
            cur = {"start": t, "kopf": z, "zeilen": [], "ende": None}
            info = (k.group(6) or "") if k else rest
            cur["kombiguide"] = (re.search(r"Kombiguide ([^|]+?)(?: \||$)", info) or [None, ""])[1].strip()
            cur["testlog"] = (re.search(r"Testlog ([\d.]+)", info) or [None, ""])[1]
        if not cur:
            continue
        cur["zeilen"].append((t, art, k, rest))
        if art == "ENDE":
            cur["ende"] = t
            out.append(cur)
            cur = None
    if cur:
        out.append(cur)
    return out


def auswerten(log):
    rows, g_rows = [], []
    for s in sitzungen(log):
        geb = defaultdict(lambda: {"sek": 0.0, "stufen": 0.0, "quests": 0, "quest_xp": 0, "tode": 0})
        z = [x for x in s["zeilen"] if x[2]]
        if len(z) < 2:
            continue
        ende = s["ende"] or z[-1][0]
        dauer = (ende - s["start"]).total_seconds()
        if dauer < MIN_SITZUNG:
            continue
        # beim Ausloggen meldet der Client Stufe und XP nicht zuverlässig (ENDE kommt mit dem letzten Kontext, Testlauf 2)
        zz = [x for x in z if x[1] != "ENDE"] or z
        von, bis = stufe(zz[0][2]), stufe(zz[-1][2])
        quests = [x for x in z if x[1] == "QUEST AB"]
        qxp = sum(int((re.search(r"\| XP (\d+)", x[3]) or [0, 0])[1]) for x in quests)
        tode = sum(1 for x in z if x[1] == "TOD")
        kenn = kennung(s["kopf"])
        for a, b in zip(z, z[1:]):
            g = (a[2].group(3) or "?").split(" > ")[0] or "?"
            key = (g, int(a[2].group(1)))
            sek = min(LUECKE, (b[0] - a[0]).total_seconds())
            e = geb[key]
            e["sek"] += sek
            if b[1] != "ENDE":
                e["stufen"] += max(0.0, stufe(b[2]) - stufe(a[2]))
        for x in z:
            g = (x[2].group(3) or "?").split(" > ")[0] or "?"
            e = geb[(g, int(x[2].group(1)))]
            if x[1] == "QUEST AB":
                e["quests"] += 1
                e["quest_xp"] += int((re.search(r"\| XP (\d+)", x[3]) or [0, 0])[1])
            elif x[1] == "TOD":
                e["tode"] += 1
        min_geb = defaultdict(float)
        for a, b in zip(z, z[1:]):
            min_geb[(a[2].group(3) or "?").split(" > ")[0] or "?"] += min(LUECKE, (b[0] - a[0]).total_seconds()) / 60
        top = ", ".join(f"{g} {m:.0f}" for g, m in sorted(min_geb.items(), key=lambda kv: -kv[1])[:3])
        rows.append({"kennung": kenn, "datum": s["start"].strftime("%Y-%m-%d"), "dauer_min": f"{dauer / 60:.0f}",
                     "stufe_von": f"{von:.2f}", "stufe_bis": f"{bis:.2f}", "stufen_pro_h": f"{(bis - von) / (dauer / 3600):.2f}",
                     "quests": len(quests), "quest_xp": qxp, "tode": tode, "gebiete": top,
                     "rxp_von": zz[0][2].group(5).strip(), "rxp_bis": zz[-1][2].group(5).strip(),
                     "kombiguide": s["kombiguide"], "testlog": s["testlog"]})
        for (g, lv), e in sorted(geb.items(), key=lambda kv: (kv[0][1], kv[0][0])):
            g_rows.append({"kennung": kenn, "datum": s["start"].strftime("%Y-%m-%d"), "gebiet": g, "stufe": lv,
                           "minuten": f"{e['sek'] / 60:.1f}", "stufen": f"{e['stufen']:.2f}", "quests": e["quests"],
                           "quest_xp": e["quest_xp"], "tode": e["tode"]})
    return rows, g_rows


def xp_zeilen(xp, stand):
    out = []
    for k, e in sorted(xp.items()):
        art, kr, gl, lv = (k.split(":") + ["?"] * 4)[:4]
        n, x, nE, xE = e["n"], e["xp"], e["nE"], e["xpE"]
        ohne = (x - xE) / (n - nE) if n > nE else None
        out.append({"art": art, "kreatur": kr, "gegnerstufe": gl, "stufe": lv, "anzahl": n, "xp": x,
                    "xp_je": f"{x / n:.1f}" if n else "", "anzahl_erholt": nE, "xp_erholt": xE,
                    "xp_je_ohne_erholt": f"{ohne:.1f}" if ohne is not None else "", "stand": stand})
    return out


def karten():
    out = {}
    if os.path.exists(KARTEN):
        for r in at._read(KARTEN):
            try:
                out[r["karte"]] = (r["name"], abs(float(r["a1"]) - float(r["a0"])), abs(float(r["b1"]) - float(r["b0"])))
            except (KeyError, ValueError):
                continue
    return out


def weg_zeilen(weg):
    """Laufweg-Proben (Testlog 3.7: «Zeit Karte x y Stufe XP XP-Max Kills Zeichen») pro Sitzung (Marke «S Zeit Version»),
    Karte und Stufe zusammenfassen."""
    km = karten()
    agg = defaultdict(lambda: defaultdict(float))
    for ch, proben in weg.items():
        prev, sitz = None, (kennung(f"{ch}|0"), 0)
        for p in proben:
            f = p.split()
            if f[0] == "S":
                prev = None   # neues Einloggen: Kills zählen neu, kein Abstand über die Lücke
                sitz = (kennung(f"{ch}|{f[1]}"), int(f[1]))
                continue
            if len(f) < 9:
                continue
            t, karte, x, y, lv, xp, mx, kills, zeichen = int(f[0]), f[1], f[2], f[3], f[4], f[5], f[6], f[7], f[8]
            cur = {"t": t, "karte": karte, "x": x, "y": y, "lv": lv, "xp": xp, "mx": mx, "kills": kills, "z": zeichen}
            if prev:
                dt = t - prev["t"]
                if 0 < dt <= WEG_LUECKE:
                    key = (sitz, prev["karte"], prev["lv"])
                    e = agg[key]
                    e["sek"] += dt
                    z = prev["z"]
                    for c, n in (("K", "kampf"), ("T", "flug"), ("D", "tot"), ("R", "erholt"), ("I", "instanz")):
                        if c in z:
                            e[n] += dt
                    if prev["karte"] == karte and prev["x"] != "-" and x != "-" and karte in km:
                        _, w, h = km[karte]
                        dx = (float(x) - float(prev["x"])) / 100 * w
                        dy = (float(y) - float(prev["y"])) / 100 * h
                        d = math.hypot(dx, dy)
                        e["yards"] += d
                        if d > 3:
                            e["bewegung"] += dt
                    if prev["lv"].isdigit() and lv.isdigit() and prev["xp"].isdigit() and xp.isdigit():
                        if lv == prev["lv"]:
                            e["xp"] += max(0, int(xp) - int(prev["xp"]))
                        elif int(lv) == int(prev["lv"]) + 1 and prev["mx"].isdigit():
                            e["xp"] += max(0, int(prev["mx"]) - int(prev["xp"])) + int(xp)
                    if prev["kills"].isdigit() and kills.isdigit():
                        e["kills"] += max(0, int(kills) - int(prev["kills"]))
            prev = cur
    out = []
    for (sitz, karte, lv), e in sorted(agg.items(), key=lambda kv: (kv[0][0][1], kv[0][2], kv[0][1])):
        name = km.get(karte, ("Instanz " + karte[1:] if karte.startswith("I") else karte, 0, 0))[0]
        out.append({"kennung": sitz[0], "datum": datetime.fromtimestamp(sitz[1]).strftime("%Y-%m-%d") if sitz[1] else "",
                    "karte": karte, "name": name, "stufe": lv, "minuten": f"{e['sek'] / 60:.1f}",
                    "bewegung_min": f"{e['bewegung'] / 60:.1f}", "kampf_min": f"{e['kampf'] / 60:.1f}",
                    "flug_min": f"{e['flug'] / 60:.1f}", "tot_min": f"{e['tot'] / 60:.1f}", "erholt_min": f"{e['erholt'] / 60:.1f}",
                    "instanz_min": f"{e['instanz'] / 60:.1f}", "yards": f"{e['yards']:.0f}", "xp": int(e["xp"]),
                    "kills": int(e["kills"])})
    return out


def dungeon_zeilen(dg):
    out = []
    for k, r in sorted(dg.items(), key=lambda kv: kv[1].get("start") or 0):
        dauer = int(r.get("dauer") or 0)
        drin = max(1, dauer - int(r.get("draussen") or 0))
        out.append({"kennung": k, "datum": datetime.fromtimestamp(int(r.get("start") or 0)).strftime("%Y-%m-%d"),
                    "instanz": r.get("id"), "name": r.get("name"), "art": r.get("art"), "dauer_min": f"{dauer / 60:.0f}",
                    "draussen_min": f"{int(r.get('draussen') or 0) / 60:.0f}", "wieder": r.get("wieder"), "xp": r.get("xp"),
                    "xp_pro_h": f"{int(r.get('xp') or 0) / (drin / 3600):.0f}", "kills": r.get("kills"),
                    "geld_kupfer": r.get("geld"), "beute": r.get("beute"), "stapel": r.get("stapel"), "tode": r.get("tode"),
                    "stufe_von": r.get("stufe0"), "stufe_bis": r.get("stufe1"), "gruppe": r.get("gruppe"), "ende": r.get("ende"),
                    "testlog": r.get("version")})
    return out


def zusammen(name, neu, schluessel):
    """Neue Zeilen mit den vorhandenen in data/spiel/<name>.csv zusammenführen (gleicher Schlüssel: neu ersetzt alt)."""
    pfad = os.path.join(D, name + ".csv")
    alt = at._read(pfad) if os.path.exists(pfad) else []
    key = lambda r: tuple(str(r.get(k, "")) for k in schluessel)
    m = {key(r): r for r in alt}
    for r in neu:
        m[key(r)] = {k: ("" if r.get(k) is None else r.get(k)) for k in F[name]}
    rows = list(m.values())
    at._write(pfad, F[name], rows)
    return rows


def bericht(sz, gb, xq, lw, dg):
    L = ["# Spieldaten: Stufen, Gebiete, XP, Laufweg, Dungeons (erzeugt von `tools/spiel_aus_testlog.py`)", "",
         "Nicht von Hand ändern: neues Testlog einlesen und neu erzeugen. Ohne Charakternamen und Uhrzeiten.", "",
         "## Quellen", "",
         "- Protokoll des Testlogs (alle Versionen): «L16 68%» in jeder Zeile = Stufe und Prozent der Stufe; QUEST AB mit XP; TOD.",
         "- Testlog 3.7: XP pro Quelle (`PLAYER_XP_UPDATE`, Quelle nach Kampf, Ziel und Quest-Abgabe), Laufweg (alle 10 s, bei "
         "Stillstand alle 60 s), Dungeon-Läufe (`IsInInstance`, `GetInstanceInfo`); APIs laut Forever-UI 1.60.1 (70374), "
         "https://github.com/Gethe/wow-ui-source/tree/forever.",
         f"- Grenzen: Zeit pro Gebiet aus dem Abstand zweier Protokollzeilen (Lücken über {LUECKE // 60} Minuten zählen als "
         f"{LUECKE // 60}); Stufen-Fortschritt aus den ganzen Prozent; Sitzungen unter {MIN_SITZUNG // 60} Minuten fehlen. "
         "Sitzungen mit Berufen, Auktionshaus oder Tests bringen wenig Stufen pro Stunde; das ist kein Mass für die Route.", ""]
    L += ["## Sitzungen", "", "| Datum | Dauer | Stufe | Stufen pro Stunde | Quests (XP) | Tode | Gebiete (Minuten) | RXP | Kombiguide |",
          "|---|---|---|---|---|---|---|---|---|"]
    for r in sorted(sz, key=lambda r: (r["datum"], r["kennung"])):
        L.append(f"| {r['datum']} | {r['dauer_min']} Min | {r['stufe_von']} → {r['stufe_bis']} | {r['stufen_pro_h']} | "
                 f"{r['quests']} ({r['quest_xp']}) | {r['tode']} | {r['gebiete']} | {r['rxp_von']} → {r['rxp_bis']} | {r['kombiguide'] or '–'} |")
    L += ["", "## Gebiete und Stufen (aus dem Protokoll, alle Sitzungen)", "",
          "| Gebiet | Stufe | Minuten | Stufen | pro Stunde | Quests (XP) | Tode | Sitzungen |", "|---|---|---|---|---|---|---|---|"]
    summe = defaultdict(lambda: {"min": 0.0, "stufen": 0.0, "q": 0, "qxp": 0, "tode": 0, "s": set()})
    for r in gb:
        e = summe[(r["gebiet"], int(r["stufe"]))]
        e["min"] += float(r["minuten"])
        e["stufen"] += float(r["stufen"])
        e["q"] += int(r["quests"])
        e["qxp"] += int(r["quest_xp"])
        e["tode"] += int(r["tode"])
        e["s"].add(r["kennung"])
    for (g, lv), e in sorted(summe.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        if e["min"] < 1:
            continue
        L.append(f"| {g} | {lv} | {e['min']:.0f} | {e['stufen']:.2f} | {e['stufen'] / (e['min'] / 60):.2f} | {e['q']} ({e['qxp']}) | "
                 f"{e['tode']} | {len(e['s'])} |")
    L += ["", "## XP pro Quelle (Testlog 3.7)", ""]
    if xq:
        L += ["«ohne erholt» = Durchschnitt der Fälle ohne erholte XP (mit erholter XP gibt ein Kill meist das Doppelte).", "",
              "| Quelle | Kreatur | Gegnerstufe | eigene Stufe | Anzahl | XP | je Fall | je Fall ohne erholt |", "|---|---|---|---|---|---|---|---|"]
        for r in sorted(xq, key=lambda r: (r["stufe"], r["art"], -int(r["anzahl"]))):
            L.append(f"| {r['art']} | {r['kreatur']} | {r['gegnerstufe']} | {r['stufe']} | {r['anzahl']} | {r['xp']} | {r['xp_je']} | "
                     f"{r['xp_je_ohne_erholt'] or '–'} |")
    else:
        L.append("Noch keine Daten (ab Testlog 3.7).")
    L += ["", "## Laufweg pro Karte und Stufe (Testlog 3.7)", ""]
    if lw:
        L += ["Bewegung = Proben mit mehr als 3 Yards Weg seit der letzten; Kampf, Flug, tot, erholt (Gasthaus/Stadt) und Instanz "
              "aus den Zeichen der Proben. Yards aus den Kartenecken (`data/karten/forever_karten.csv`).", "",
              "| Karte | Stufe | Minuten | Bewegung | Kampf | Flug | tot | erholt | Yards pro Min | XP pro Stunde | Kills |",
              "|---|---|---|---|---|---|---|---|---|---|---|"]
        s_lw = defaultdict(lambda: defaultdict(float))
        for r in lw:
            e = s_lw[(r["name"], r["stufe"])]
            for f in ("minuten", "bewegung_min", "kampf_min", "flug_min", "tot_min", "erholt_min", "yards", "xp", "kills"):
                e[f] += float(r[f] or 0)
        for (name, lv), e in sorted(s_lw.items(), key=lambda kv: (int(kv[0][1]) if str(kv[0][1]).isdigit() else 0, kv[0][0])):
            if e["minuten"] < 1:
                continue
            L.append(f"| {name} | {lv} | {e['minuten']:.0f} | {e['bewegung_min']:.0f} | {e['kampf_min']:.0f} | {e['flug_min']:.0f} | "
                     f"{e['tot_min']:.0f} | {e['erholt_min']:.0f} | {e['yards'] / e['minuten']:.0f} | {e['xp'] / (e['minuten'] / 60):.0f} | "
                     f"{e['kills']:.0f} |")
    else:
        L.append("Noch keine Daten (ab Testlog 3.7).")
    L += ["", "## Dungeon-Läufe (Testlog 3.7)", ""]
    if dg:
        L += ["| Datum | Dungeon | Dauer (draussen) | XP | XP pro Stunde drin | Kills | Geld | Stapel Beute | Tode | Stufe | Gruppe | Ende |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for r in sorted(dg, key=lambda r: r["datum"]):
            geld = at.silber(int(r["geld_kupfer"]) / 100) if str(r.get("geld_kupfer") or "").lstrip("-").isdigit() else "–"
            L.append(f"| {r['datum']} | {r['name']} | {r['dauer_min']} Min ({r['draussen_min']}) | {r['xp']} | {r['xp_pro_h']} | "
                     f"{r['kills']} | {geld} | {r['stapel']} | {r['tode']} | {r['stufe_von']} → {r['stufe_bis']} | {r['gruppe']} | {r['ende']} |")
    else:
        L.append("Noch keine Daten (ab Testlog 3.7).")
    L.append("")
    os.makedirs(os.path.dirname(BERICHT), exist_ok=True)
    open(BERICHT, "w", encoding="utf-8").write("\n".join(L))


def main():
    pfade = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not pfade:
        raise SystemExit("Aufruf: python3 tools/spiel_aus_testlog.py <KombiTestlog.lua> [weitere …]")
    log, weg, xp, dg = lade(pfade)
    stand = log[-1][0].strftime("%Y-%m-%d") if log else ""
    sz_neu, gb_neu = auswerten(log)
    os.makedirs(D, exist_ok=True)
    sz = zusammen("sitzungen", sz_neu, ["kennung"])
    gb = zusammen("gebiete", gb_neu, ["kennung", "gebiet", "stufe"])
    xq = zusammen("xp_quellen", xp_zeilen(xp, stand), ["art", "kreatur", "gegnerstufe", "stufe"]) if xp else \
        (at._read(os.path.join(D, "xp_quellen.csv")) if os.path.exists(os.path.join(D, "xp_quellen.csv")) else [])
    lw = zusammen("laufweg", weg_zeilen(weg), ["kennung", "karte", "stufe"]) if weg else \
        (at._read(os.path.join(D, "laufweg.csv")) if os.path.exists(os.path.join(D, "laufweg.csv")) else [])
    dgr = zusammen("dungeons", dungeon_zeilen(dg), ["kennung"]) if dg else \
        (at._read(os.path.join(D, "dungeons.csv")) if os.path.exists(os.path.join(D, "dungeons.csv")) else [])
    bericht(sz, gb, xq, lw, dgr)
    print(f"{len(log)} Protokollzeilen, {len(sz_neu)} Sitzungen, {len(gb_neu)} Gebiet/Stufe, {len(xp)} XP-Quellen, "
          f"{sum(len(v) for v in weg.values())} Laufweg-Proben, {len(dg)} Dungeon-Läufe")
    print("Bericht:", os.path.relpath(BERICHT, ROOT))


if __name__ == "__main__":
    main()
