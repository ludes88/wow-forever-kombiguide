# Eigene AH-Preise aus dem Testlog übernehmen (Testlog 3.5, AH-Scan).
#
# Aufruf:  python3 tools/ah_aus_testlog.py <KombiTestlog.lua oder Text von /tl zeigen> [--eintragen]
#
# Liest die AH-Scans: aus der SavedVariables-Datei KombiTestlogDB.ahScans (vollständig, mit Preisstufen), sonst die
# Zeilen «AH-SCAN» aus dem Text von /tl zeigen (nur die Gegenstände des Plans, ohne Preisstufen). Schreibt:
#   data/preise/ah_eigen.csv   pro Scan und Gegenstand des Plans: Tiefstpreis, Median, Menge, Angebote und was die
#                              billigsten 20 und 100 Stück kosten. Neue Scans kommen dazu, alte bleiben: daraus die Wochenpreise.
#   data/preise/ah_alle.csv    der letzte Scan mit allen Gegenständen (Tiefstpreis, Median, Menge, Angebote)
#   docs/plan/ah-preise.md     Bericht: Scans und Plan-Gegenstände mit AHledger-Preis, Median und 7-Tage-Median
# --eintragen  schreibt den 7-Tage-Median der eigenen Scans (Markt des letzten Scans) als «Eigener Preis (s)» und
#              «Rechenpreis (s)» in data/rechnung/Preise.csv und als preis_s in die AH-Zeilen von data/kombi/preise_zusatz.csv.
#              Nur aus vollständigen Scans und nur, wenn im Mittel mindestens MIN_MENGE Stück im Angebot waren.
#              Danach tools/plan_berufe.py laufen lassen. Händlerware bleibt beim Händlerpreis, die 30-Tage-Spalte und
#              die xlsx bleiben bei AHledger.
#
# Datenschutz: Die Testlog-Datei enthält Charakter- und Realmnamen und kommt nie ins Repo. Ins Repo kommen nur Datum,
# Region, Fraktion, ein Kurzzeichen für den Realm und Preise. Das Kurzzeichen trennt die Realms, ohne den Namen zu
# schreiben; wer alle Realmnamen durchprobiert, kann es zurückrechnen. Markt «Beta» vor dem Start am 04.11.2026, danach
# «Live» (Start laut https://www.warcrafttavern.com/forever/guides/beta/, geprüft am 13.10.2026).
# Preise im Testlog in Kupfer, in den Tabellen in Silber (wie data/rechnung/Preise.csv).
import csv, hashlib, io, os, re, statistics, sys
from datetime import datetime, timedelta

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
D = os.path.join(ROOT, "data")
EIGEN = os.path.join(D, "preise", "ah_eigen.csv")
ALLE = os.path.join(D, "preise", "ah_alle.csv")
BERICHT = os.path.join(ROOT, "docs", "plan", "ah-preise.md")
PREISE = os.path.join(D, "rechnung", "Preise.csv")
ZUSATZ = os.path.join(D, "kombi", "preise_zusatz.csv")
START_LIVE = "2026-11-04"
UNVOLLSTAENDIG = 0.10   # mehr als 10 % der Angebote ohne Daten: Scan zählt nicht für den Plan (wie die Warnung im Testlog)
MIN_MENGE = 50          # «Schwelle dünner Markt» aus data/rechnung/Uebersicht.csv (Wahl von Claude vom 12.10., änderbar)
F_EIGEN = ["datum", "markt", "item_id", "material", "deutsch", "tiefstpreis_s", "median_s", "menge", "angebote",
           "kosten_20_s", "kosten_100_s", "hinweis", "quelle"]
F_ALLE = ["datum", "markt", "item_id", "material", "tiefstpreis_s", "median_s", "menge", "angebote"]
USAGE = "Aufruf: python3 tools/ah_aus_testlog.py <KombiTestlog.lua oder Text von /tl zeigen> [--eintragen]"


# --- Lesen ------------------------------------------------------------------------------------------------------------
def _lua_tabelle(text):
    """SavedVariables-Datei (Text, kein Bytecode) in einer leeren Lua-Umgebung ausführen. Die Datei schreibt der Client;
    die leere Umgebung hält os und io fern, ist aber kein vollständiger Schutz (keine Zeit- und Speichergrenze)."""
    from lupa import lua51
    L = lua51.LuaRuntime(unpack_returned_tuples=True)
    run = L.eval("""function(src)
        if src:byte(1) == 27 then return nil, "Bytecode wird nicht geladen" end
        local f, err = loadstring(src, "SavedVariables")
        if not f then return nil, err end
        local env = {}
        setfenv(f, env)
        local ok, e = pcall(f)
        if not ok then return nil, e end
        return env.KombiTestlogDB
    end""")
    res = run(text)
    db = res[0] if isinstance(res, tuple) else res
    if db is None:
        raise SystemExit("Datei liess sich nicht lesen: " + str(res[1] if isinstance(res, tuple) else "?"))
    return db


def _py(v):
    """Lua-Tabelle -> dict bzw. list (Schlüssel 1..n). Ganzzahlige Schlüssel als int (Lua 5.1 kennt nur Gleitkomma)."""
    if hasattr(v, "items") and not isinstance(v, (str, bytes)):
        d = {(int(k) if isinstance(k, float) and k.is_integer() else k): _py(x) for k, x in v.items()}
        if d and all(isinstance(k, int) for k in d) and sorted(d) == list(range(1, len(d) + 1)):
            return [d[i] for i in range(1, len(d) + 1)]
        return d
    return v


def phase(datum):
    return "Live" if datum[:10] >= START_LIVE else "Beta"


def kennung(realm):
    """Kurzzeichen für den Realm: trennt Realms, ohne den Namen ins Repo zu schreiben."""
    if not realm or realm == "?":
        return "R?"
    return "R" + hashlib.sha256(realm.encode("utf-8")).hexdigest()[:4]


def _stufen(s):
    out = []
    for teil in (s or "").split(","):
        if "*" in teil:
            u, c = teil.split("*")
            out.append((int(float(u)), int(float(c))))
    return out


def _kompakt(s, plan):
    """«ID:Tiefstpreis:Median:Menge:Angebote;…» (Kupfer) -> {ID: Preise}."""
    out = {}
    for teil in (s or "").split(";"):
        f = teil.split(":")
        if len(f) == 5:
            i, lo, med, menge, ang = (int(float(x)) for x in f)
            out[i] = {"tiefst": lo, "median": med, "menge": menge, "angebote": ang, "stufen": None, "plan": plan}
    return out


def _aus_lua(db):
    scans = []
    for r in db.get("ahScans") or []:
        preise = _kompakt(r.get("alle"), False)          # fehlt bei älteren Scans (nur die 10 neuesten behalten alles)
        preise.update(_kompakt(r.get("plan"), True))
        for i, s in (r.get("stufen") or {}).items():
            if int(i) in preise:
                preise[int(i)]["stufen"] = _stufen(s)
        datum = str(r.get("datum", "?"))
        n, fehlend = r.get("angebote") or 0, r.get("fehlend") or 0
        scans.append({"datum": datum, "zeit": int(r.get("zeit") or 0),
                      "markt": f"{r.get('region', '?')} {r.get('fraktion', '?')} {kennung(r.get('realm'))}",
                      "phase": phase(datum), "client": r.get("client", "-"), "angebote": n,
                      "gegenstaende": r.get("gegenstaende"), "nur_gebot": r.get("nurGebot"), "fehlend": fehlend,
                      "unvollstaendig": n > 0 and fehlend > n * UNVOLLSTAENDIG,
                      "dauer": r.get("dauer"), "quelle": "Testlog-Datei", "preise": preise})
    return scans


MONEY = re.compile(r"^(?:(\d+)g)? ?(?:(\d+)s)? ?(?:(\d+)c)?$")
ZEILE = re.compile(r"\| AH-SCAN \|.*?\| Scan (?P<datum>\d{4}-\d\d-\d\d \d\d:\d\d) \| (?P<region>\S+) (?P<fraktion>\S+) \| "
                   r"Realm (?P<realm>.+?) \| (?P<angebote>\d+) Angebote, (?P<gegen>\d+) Gegenstände, (?P<gebot>\d+) nur mit Gebot, "
                   r"(?P<dauer>\d+) s(?P<warn>.*?)\| Tiefstpreis / Median / Stück: (?P<liste>.*?)\"?,?\s*(?:--.*)?$", re.M)
EINTRAG = re.compile(r"^(?:(?P<name>.+) \((?P<id>\d+)\)|(?P<id2>\d+)) (?P<lo>[\dgsc ]+?) / (?P<med>[\dgsc ]+?) / (?P<menge>\d+)$")


def kupfer(text):
    m = MONEY.match(text.strip())
    if not m or not any(m.groups()):
        raise ValueError("kein Geldbetrag: " + text)
    g, s, c = (int(x) if x else 0 for x in m.groups())
    return g * 10000 + s * 100 + c


def _aus_text(text):
    scans = []
    for m in ZEILE.finditer(text.replace('\\"', '"')):
        preise, namen = {}, {}
        for teil in m.group("liste").split("; "):
            e = EINTRAG.match(teil.strip())
            if not e:
                continue
            i = int(e.group("id") or e.group("id2"))
            preise[i] = {"tiefst": kupfer(e.group("lo")), "median": kupfer(e.group("med")), "menge": int(e.group("menge")),
                         "angebote": None, "stufen": None, "plan": True}
            if e.group("name"):
                namen[i] = e.group("name")
        datum = m.group("datum")
        scans.append({"datum": datum, "zeit": 0, "markt": f"{m.group('region')} {m.group('fraktion')} {kennung(m.group('realm'))}",
                      "phase": phase(datum), "client": "-", "angebote": int(m.group("angebote")),
                      "gegenstaende": int(m.group("gegen")), "nur_gebot": int(m.group("gebot")), "fehlend": None,
                      "unvollstaendig": "unvollständig" in m.group("warn"), "dauer": int(m.group("dauer")),
                      "quelle": "Text von /tl zeigen", "preise": preise, "namen": namen})
    return scans


def lese(text):
    """Scans aus der SavedVariables-Datei (bevorzugt) oder aus dem Text von /tl zeigen. Ohne Realm- und Charakternamen."""
    if re.search(r"^\s*KombiTestlogDB\s*=", text, re.M):
        db = _py(_lua_tabelle(text))
        scans = _aus_lua(db)
        namen = {}
        for z in _aus_text("\n".join(db.get("log") or [])):   # deutsche Namen aus den AH-SCAN-Zeilen
            namen.update(z["namen"])
        for s in scans:
            s["namen"] = namen
        if scans:
            return scans
    return _aus_text(text)


def kosten(stufen, n):
    """Kosten der billigsten n Stück aus den Preisstufen: (Kupfer, Stück, die es gibt, höchstens n)."""
    total, got = 0, 0
    for u, c in stufen:
        take = min(c, n - got)
        total += take * u
        got += take
        if got >= n:
            break
    return total, got


def kosten_text(p, n):
    """Kosten für n Stück als Text in Silber. Reichen die gespeicherten Preisstufen (höchstens 100 pro Gegenstand) nicht,
    obwohl mehr im Angebot ist: Untergrenze mit dem höchsten bekannten Preis für den Rest."""
    if not p["stufen"]:
        return ""
    k, got = kosten(p["stufen"], n)
    if got >= n:
        return f"{k / 100:.2f}"
    if p["menge"] >= n:
        return f"mind. {(k + (n - got) * p['stufen'][-1][0]) / 100:.2f}"
    return f"nur {p['menge']} Stück"


# --- Namen und Plan-Preise ----------------------------------------------------------------------------------------------
def _read(path, skip=0):
    with open(path, encoding="utf-8-sig", newline="") as f:
        lines = f.read().splitlines()
    return list(csv.DictReader(lines[skip:], delimiter=";"))


def plan_items():
    """Item-ID -> {material, deutsch, plan_s (Rechenpreis), ahledger_s (NH Median), haendler} aus den Plan-Tabellen."""
    out = {}
    neu = lambda m: {"material": m, "deutsch": "", "plan_s": None, "ahledger_s": None, "haendler": False}
    for r in _read(os.path.join(D, "kombi", "items.csv"), skip=1):
        if r.get("item_id", "").strip().isdigit():
            out[int(r["item_id"])] = dict(neu(r["name"]), deutsch=r.get("deutsch") or "")
    for r in _read(PREISE, skip=1):
        m = re.search(r"ahledger\.com/items/(\d+)-", r.get("Quelle") or "")
        if not m or not r.get("Material"):
            continue
        e = out.setdefault(int(m.group(1)), neu(r["Material"]))
        if (r.get("Händlerpreis (s)") or "").strip():
            e["plan_s"], e["haendler"] = float(r["Händlerpreis (s)"]), True
        else:
            if (r.get("Rechenpreis (s)") or "").strip():
                e["plan_s"] = float(r["Rechenpreis (s)"])
            if (r.get("NH Median (s)") or "").strip():
                e["ahledger_s"] = float(r["NH Median (s)"])
    for r in _read(ZUSATZ):
        if r.get("item_id", "").strip().isdigit():
            e = out.setdefault(int(r["item_id"]), neu(r["material"]))
            e["plan_s"], e["haendler"] = float(r["preis_s"]), r["art"] == "Händler"
    return out


def s2(kupfer_):
    return "" if kupfer_ is None else f"{kupfer_ / 100:.2f}"


def silber(s):
    if s is None:
        return "–"
    g, r = divmod(round(s * 100), 10000)
    sv, k = divmod(r, 100)
    parts = [f"{g}g"] * bool(g) + [f"{sv}s"] * bool(sv) + [f"{k}c"] * bool(k or not (g or sv))
    return " ".join(parts)


def silber_text(t):
    """Wert aus ah_eigen.csv (Silber, «mind. x» oder «nur x Stück») lesbar machen."""
    if not t:
        return "–"
    if t.startswith("mind. "):
        return "mind. " + silber(float(t[6:]))
    if t.startswith("nur "):
        return t
    return silber(float(t))


# --- Schreiben -----------------------------------------------------------------------------------------------------------
def _write(path, fields, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=fields, delimiter=";", lineterminator="\n", extrasaction="ignore")
    w.writeheader()
    for r in rows:
        w.writerow({k: ("" if r.get(k) is None else str(r.get(k))).replace(";", ",") for k in fields})
    open(path, "w", encoding="utf-8", newline="").write(buf.getvalue())


def zeilen_eigen(scans, plan):
    rows = []
    for s in scans:
        markt = f"{s['markt']} {s['phase']}"
        for i, p in sorted(s["preise"].items()):
            if not p["plan"]:
                continue   # nur Gegenstände des Plans; alle anderen stehen für den letzten Scan in ah_alle.csv
            info = plan.get(i, {})
            rows.append({"datum": s["datum"], "markt": markt, "item_id": i, "material": info.get("material", ""),
                         "deutsch": s.get("namen", {}).get(i) or info.get("deutsch", ""),
                         "tiefstpreis_s": s2(p["tiefst"]), "median_s": s2(p["median"]), "menge": p["menge"],
                         "angebote": p["angebote"], "kosten_20_s": kosten_text(p, 20), "kosten_100_s": kosten_text(p, 100),
                         "hinweis": "unvollständig" if s["unvollstaendig"] else "",
                         "quelle": f"Testlog 3.5, eigener AH-Scan ({s['quelle']})"})
    return rows


def zusammenfuehren(neu):
    """Neue Zeilen in ah_eigen.csv übernehmen. Gleicher Scan (Datum, Markt, Item): nur Felder mit Wert ersetzen,
    damit z. B. der Text von /tl zeigen die Preisstufen aus der Datei nicht löscht."""
    alt = _read(EIGEN) if os.path.exists(EIGEN) else []
    key = lambda r: (r["datum"], r["markt"], str(r["item_id"]))
    merged = {key(r): r for r in alt}
    for r in neu:
        k = key(r)
        if k in merged:
            neu_werte = {f: v for f, v in r.items() if v not in (None, "")}
            if "Testlog-Datei" in merged[k].get("quelle", ""):
                neu_werte.pop("quelle", None)   # die Datei ist die vollständigere Quelle
            merged[k] = {**merged[k], **neu_werte}
        else:
            merged[k] = r
    return sorted(merged.values(), key=lambda r: (r["datum"], r["markt"], int(r["item_id"]))), len(merged) - len(alt)


def wochen_median(rows, markt):
    """Pro Item-ID aus den vollständigen Scans dieses Markts in den 7 Tagen bis zum letzten Scan:
    (Median der Scan-Mediane, Anzahl Scans, Median der Menge). Dazu das Datum des letzten Scans."""
    eigene = [r for r in rows if r["markt"] == markt and r["median_s"] and r.get("hinweis", "") != "unvollständig"]
    if not eigene:
        return {}, None
    letzt = max(r["datum"] for r in eigene)
    grenze = (datetime.strptime(letzt, "%Y-%m-%d %H:%M") - timedelta(days=7)).strftime("%Y-%m-%d %H:%M")
    werte = {}
    for r in eigene:
        if r["datum"] >= grenze:
            werte.setdefault(int(r["item_id"]), []).append((float(r["median_s"]), int(float(r["menge"] or 0))))
    return {i: (statistics.median(m for m, _ in v), len(v), statistics.median(q for _, q in v)) for i, v in werte.items()}, letzt


def bericht(scans, rows, plan, eingetragen):
    letzter = max(scans, key=lambda s: (s["datum"], s["zeit"]))
    markt = f"{letzter['markt']} {letzter['phase']}"
    woche, _ = wochen_median(rows, markt)
    alle_scans = sorted({(r["datum"], r["markt"]) for r in rows})
    eig = {int(r["item_id"]): r for r in rows if r["datum"] == letzter["datum"] and r["markt"] == markt}
    L = ["# Eigene AH-Preise (erzeugt von `tools/ah_aus_testlog.py`)", "",
         "Nicht von Hand ändern: neues Testlog einlesen und neu erzeugen.", "",
         "## Quellen", "",
         "- Eigene Scans mit Testlog 3.5: `C_AuctionHouse.ReplicateItems` laut Forever-UI 1.60.1 (70374), "
         "`Blizzard_APIDocumentationGenerated/AuctionHouseDocumentation.lua` (https://github.com/Gethe/wow-ui-source/tree/forever). "
         "Werte: `data/preise/ah_eigen.csv` (Plan-Gegenstände, alle Scans), `data/preise/ah_alle.csv` (letzter Scan, alle Gegenstände).",
         "- Vergleich: AHledger, Forever-Beta, Median Normal Horde US (`data/rechnung/Preise.csv`, Spalte «NH Median (s)»).",
         "- Grenze Beta/Live: Start am 04.11.2026 (https://www.warcrafttavern.com/forever/guides/beta/, geprüft am 13.10.2026).",
         "- Median = Preis pro Stück, bei dem die Hälfte der angebotenen Stückzahl erreicht ist (nach Stückzahl gewichtet). "
         "7 Tage = Median der Scan-Mediane der letzten 7 Tage bis zum letzten Scan, gleicher Markt, nur vollständige Scans. "
         f"«dünn» = im Mittel weniger als {MIN_MENGE} Stück im Angebot (Schwelle aus `data/rechnung/Uebersicht.csv`).",
         "- Markt = Region, Fraktion, Kurzzeichen des Realms (statt des Namens), Beta oder Live.", "",
         "## Scans", "", "| Datum | Markt | Angebote | Gegenstände | nur mit Gebot | Dauer | gelesen aus | Hinweis |",
         "|---|---|---|---|---|---|---|---|"]
    for s in sorted(scans, key=lambda s: s["datum"]):
        L.append(f"| {s['datum']} | {s['markt']} {s['phase']} | {s['angebote']} | {s['gegenstaende']} | {s['nur_gebot']} | "
                 f"{s['dauer']} s | {s['quelle']} | {'unvollständig, zählt nicht für den Plan' if s['unvollstaendig'] else ''} |")
    L += ["", f"Insgesamt {len(alle_scans)} Scans in `data/preise/ah_eigen.csv`.", "",
          f"## Plan-Gegenstände im letzten Scan ({letzter['datum']}, {markt})", "",
          "Abweichung = 7-Tage-Median gegenüber dem AHledger-Median (Normal Horde US). «nur X Stück»: so viel war im Angebot; "
          "«mind.»: mehr Stück als gespeicherte Preisstufen, der Rest ist mit dem höchsten bekannten Preis gerechnet.", "",
          "| Material | ID | AHledger | Tiefstpreis | Median | 7 Tage (Scans) | Menge | 100 Stück kosten | Abweichung | Plan |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    fehlt = []
    for i, info in sorted(plan.items(), key=lambda kv: kv[1]["material"]):
        if info["haendler"]:
            continue
        p = letzter["preise"].get(i)
        if not p:
            fehlt.append(f"{info['material']} ({i})")
            continue
        w = woche.get(i)
        basis = info["ahledger_s"]
        abw = "–" if not (basis and w) else f"{(w[0] - basis) / basis * 100:+.0f} %"
        nutzbar = "dünn" if w and w[2] < MIN_MENGE else ("–" if not w else "ja")
        name = info["material"] + (f" ({letzter.get('namen', {}).get(i)})" if letzter.get("namen", {}).get(i) else "")
        L.append(f"| {name} | {i} | {silber(basis)} | {silber(p['tiefst'] / 100)} | {silber(p['median'] / 100)} | "
                 f"{silber(w[0]) + f' ({w[1]})' if w else '–'} | {p['menge']} | {silber_text(eig.get(i, {}).get('kosten_100_s', ''))} | "
                 f"{abw} | {nutzbar} |")
    if fehlt:
        L += ["", "Nicht im Angebot: " + ", ".join(fehlt) + "."]
    L += ["", "Spalte «Plan»: «ja» = mit `--eintragen` übernehmbar, «dünn» = bleibt beim AHledger-Preis.", "",
          "## Im Plan", "",
          (f"Eingetragen: {eingetragen} Preise (7-Tage-Median dieses Markts) als «Eigener Preis (s)» und «Rechenpreis (s)» in "
           "`data/rechnung/Preise.csv` und in den AH-Zeilen von `data/kombi/preise_zusatz.csv`; `tools/plan_berufe.py` rechnet "
           "damit. Die 30-Tage-Spalte und die xlsx bleiben bei AHledger."
           if eingetragen else
           "Noch nicht eingetragen: Der Plan rechnet weiter mit den AHledger-Preisen. Eintragen mit "
           "`python3 tools/ah_aus_testlog.py <Testlog> --eintragen`, danach `python3 tools/plan_berufe.py` "
           "(offene Entscheidung 17)."), ""]
    os.makedirs(os.path.dirname(BERICHT), exist_ok=True)
    open(BERICHT, "w", encoding="utf-8").write("\n".join(L))


def eintragen(rows, markt):
    """7-Tage-Median als eigenen Preis in Preise.csv und preise_zusatz.csv (AH-Zeilen), nur nicht dünne Gegenstände.
    Gibt die Anzahl geänderter Zeilen zurück."""
    woche, letzt = wochen_median(rows, markt)
    woche = {i: w for i, w in woche.items() if w[2] >= MIN_MENGE}
    if not woche:
        return 0
    notiz = lambda w: f"eigener Scan {markt}, 7 Tage bis {letzt}, {w[1]} Scans, Menge {w[2]:.0f}"
    n = 0
    raw = open(PREISE, encoding="utf-8", newline="").read().split("\n")
    kopf, rest = raw[0], raw[1:]
    reader = list(csv.reader(rest, delimiter=";"))
    head = reader[0]
    ci = {h: j for j, h in enumerate(head)}
    for row in reader[1:]:
        if len(row) <= ci["Quelle"] or not row[0]:
            continue
        m = re.search(r"ahledger\.com/items/(\d+)-", row[ci["Quelle"]])
        if not m or row[ci["Händlerpreis (s)"]].strip() or int(m.group(1)) not in woche:
            continue
        w = woche[int(m.group(1))]
        row += [""] * (len(head) - len(row))   # nur geänderte Zeilen auffüllen (Bemerkung fehlt oft)
        row[ci["Eigener Preis (s)"]] = row[ci["Rechenpreis (s)"]] = f"{w[0]:.2f}"
        bem = re.sub(r"\s*·?\s*eigener Scan [^·]*", "", row[ci["Bemerkung"]]).strip(" ·")
        row[ci["Bemerkung"]] = (bem + " · " if bem else "") + notiz(w)
        n += 1
    buf = io.StringIO()
    csv.writer(buf, delimiter=";", lineterminator="\n").writerows(reader)
    open(PREISE, "w", encoding="utf-8", newline="").write(kopf + "\n" + buf.getvalue().rstrip("\n") + "\n")
    zus = _read(ZUSATZ)
    for r in zus:
        if r["art"] == "AH" and r["item_id"].isdigit() and int(r["item_id"]) in woche:
            w = woche[int(r["item_id"])]
            r["preis_s"] = f"{w[0]:.2f}"
            r["quelle"] = re.sub(r"\s*·\s*eigener Scan .*$", "", r["quelle"]) + " · " + notiz(w)
            n += 1
    _write(ZUSATZ, list(zus[0].keys()), zus)
    return n


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        raise SystemExit(USAGE)
    text = open(args[0], encoding="utf-8", errors="replace").read()
    scans = lese(text)
    if not scans:
        print("Keine AH-Scans gefunden (Testlog 3.5: Auktionshaus öffnen oder /tl ah, danach /reload).")
        return
    plan = plan_items()
    rows, neu = zusammenfuehren(zeilen_eigen(scans, plan))
    _write(EIGEN, F_EIGEN, rows)
    letzter = max(scans, key=lambda s: (s["datum"], s["zeit"]))
    markt = f"{letzter['markt']} {letzter['phase']}"
    if letzter["quelle"] == "Testlog-Datei" and any(not p["plan"] for p in letzter["preise"].values()):
        alle = [{"datum": letzter["datum"], "markt": markt, "item_id": i, "material": plan.get(i, {}).get("material", ""),
                 "tiefstpreis_s": s2(p["tiefst"]), "median_s": s2(p["median"]), "menge": p["menge"], "angebote": p["angebote"]}
                for i, p in sorted(letzter["preise"].items())]
        _write(ALLE, F_ALLE, alle)
    n = eintragen(rows, markt) if "--eintragen" in sys.argv else 0
    bericht(scans, rows, plan, n)
    unv = sum(1 for s in scans if s["unvollstaendig"])
    print(f"{len(scans)} Scans gelesen ({letzter['quelle']}{f', {unv} unvollständig' if unv else ''}), letzter {letzter['datum']} "
          f"{markt}: {letzter['angebote']} Angebote, {letzter['gegenstaende']} Gegenstände")
    print(f"{os.path.relpath(EIGEN, ROOT)}: {len(rows)} Zeilen ({neu} neu)")
    if "--eintragen" in sys.argv:
        print(f"eingetragen: {n} Preise (7 Tage, {markt}, nur mit mindestens {MIN_MENGE} Stück); jetzt python3 tools/plan_berufe.py")
    print("Bericht:", os.path.relpath(BERICHT, ROOT))


if __name__ == "__main__":
    main()
