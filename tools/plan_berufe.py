# Berufe-Plan zum Wechsel in Orgrimmar: Sweetspot für eigenes Leder, Lederverarbeitung (LW) und Verzauberkunst (VZ) bis 150
# mit Stückzahlen, Einkauf (AH und Händler), Entzaubern und Verkauf. Rechnet in Stufen A-D, damit der Guide nach Gold staffeln kann.
#
# Aufruf: python3 tools/plan_berufe.py [Bericht.md]        (Standard: docs/plan/berufe-plan.md)
# Eingaben (alle mit Quelle pro Zeile):
#   tools/plan_mengen.py               Modell der Route: Bestand an Leder, Fetzen und Bälgen beim Wechsel (Abschnitt WECHSEL)
#   data/kombi/bedarf_lw_vz.csv        LW- und VZ-Route 1-150 (wow-professions, Forever-Beta), Varianten ab LW 130
#   data/kombi/rezepte.csv             Farben (Lernstufe) der Rezepte laut AHledger, für die Widerspruchsprüfung
#   data/kombi/items.csv               Item-IDs und deutsche Namen (nur im Testlog gesehene)
#   data/kombi/preise_zusatz.csv       Händlerpreise und AH-Preise, die in Preise.csv fehlen
#   data/rechnung/Preise.csv           AH-Rechenpreise (AHledger, Beta, Normal Horde US): «jetzt» und Median 30 Tage
#   data/rechnung/Kreislauf.csv        Entzaubern: Staub, Essenz und Splitter pro grünem LW-Teil (Erwartungswert)
#   data/kombi/lehrer.csv              Lernstufen und Kosten der Lehrer in Orgrimmar (Testlog 15.10., tools/lehrer_aus_testlog.py)
#   data/kombi/rezepte_de.csv          englischer und deutscher Rezeptname, Zauber-ID (Zuordnung zu den Lehrerlisten)
#   data/preise/haendler_ankauf.csv    was der Händler im Forever-Client zahlt (Testlog 3.6/3.7, tools/ah_aus_testlog.py)
#
# Begriffe: «eigen» = Bestand beim Wechsel (untere Rate des Modells, also vorsichtig gerechnet); alles andere wird gekauft.
# Stufe A = Kern der Sitzung in Orgrimmar (billig, nutzt das eigene Leder); B in Orgrimmar oder Thunder Bluff, C und D in Thunder Bluff, je nach Gold.
import csv, math, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plan_mengen as pm  # noqa: E402  (Modell der Route; der Bericht von plan_mengen entsteht dabei nicht)

ROOT, D = pm.ROOT, os.path.join(pm.ROOT, "data")
num, read, silber = pm.num, pm.read, pm.silber

# KONSTANTEN mit Quelle
STUFEN = [("A", 80, 50, "Kern in Orgrimmar: eigenes Leder verarbeiten"),          # (Stufe, LW bis, VZ bis, Zweck)
          ("B", 100, 100, "in Orgrimmar, wenn das Gold reicht, sonst in Thunder Bluff"),
          ("C", 130, 130, "in Thunder Bluff, Stufe 20"),
          ("D", 150, 150, "in Thunder Bluff, der teure Rest bis 150")]
FLB_BEHALTEN = 10        # wow-professions: «Keep 10 of the belts for the Dark Leather Belts at 115.»
ANGELN_FAENGE_H = 3600 / (349 / 13)   # Testlog 13.10.: 14 Fänge, vom ersten bis zum letzten 349 s = 13 Abstände (Stonebull Lake,
                                      # Angeln 1-15); bis 15.10. stand hier 349/14 (7,7 % zu hoch, Prüfbericht 15.10.)
DEVIATE_ANTEIL = 0.35                 # AHledger, Item 6522: Lushwater Oasis «35% of 153 looted»
DEVIATE_PH = 10.99                    # AHledger, Item 6522: Median PvP Horde US (Scan 13.10.2026); Normal Horde US steht in preise_zusatz.csv
SCHLEIFEN = {"Light Leather": "Ruined Leather Scraps"}   # Rezept, das ein Material herstellt, das die Route später braucht
# Zauberstäbe als Weg für VZ (Vorschlag von Claude vom 15.10., nicht im Plan, Abschnitt 9 des Berichts): orange bis «gelb ab»
# laut SeeMeta, Enchanting (Stand 14.10.2026, https://seemeta.com/en/wow-forever/professions/enchanting: Lesser Magic Wand
# gelb 75, grün 95, grau 115; Greater Magic Wand gelb 110, grün 130, grau 150). Bei VZ 100 im Testlog 15.10. bestätigt:
# Lesser grün, Greater orange. Reagenzien aus dem Testlog (REZEPTE), Händlerpreis aus haendler_ankauf.csv, Lernstufe und
# Kosten aus lehrer.csv. Orange = jede Herstellung gibt einen Punkt.
STAEBE = [("Lesser Magic Wand", 10, 75, {"Simple Wood": 1, "Lesser Magic Essence": 1}),
          ("Greater Magic Wand", 70, 110, {"Simple Wood": 1, "Lesser Magic Essence": 2})]


def items():
    rows = read(os.path.join(D, "kombi", "items.csv"), skip=1)
    return {r["name"]: r for r in rows}


def prices():
    """Rechenpreise in Silber: «jetzt» (Preise.csv Rechenpreis) und «30 Tage» (Median 30 Tage); Händlerware zum Händlerpreis."""
    now, d30, vendor = {}, {}, set()
    for r in read(os.path.join(D, "rechnung", "Preise.csv"), skip=1):
        m = r.get("Material")
        if not m:
            continue
        hp = num(r["Händlerpreis (s)"])
        if hp:
            now[m] = d30[m] = hp
            vendor.add(m)
        elif r["Rechenpreis (s)"].strip():
            now[m] = num(r["Rechenpreis (s)"])
            d30[m] = num(r["NH 30 Tage (s)"]) or now[m]
    for r in read(os.path.join(D, "kombi", "preise_zusatz.csv")):
        now[r["material"]], d30[r["material"]] = num(r["preis_s"]), num(r["preis_30d_s"])
        if r["art"] == "Händler":
            vendor.add(r["material"])
    return now, d30, vendor


def eigene_preise():
    """Materialien, für die tools/ah_aus_testlog.py --eintragen einen eigenen Preis gesetzt hat (Spalte «Eigener Preis (s)»)."""
    out = [r["Material"] for r in read(os.path.join(D, "rechnung", "Preise.csv"), skip=1)
           if r.get("Material") and (r.get("Eigener Preis (s)") or "").strip()]
    out += [r["material"] for r in read(os.path.join(D, "kombi", "preise_zusatz.csv")) if "eigener Scan" in (r.get("quelle") or "")]
    return out


def de_table():
    """Entzaubern pro Teil (Erwartungswert) aus Kreislauf.csv: {Teil: {Material: Menge}}."""
    lines = open(os.path.join(D, "rechnung", "Kreislauf.csv"), encoding="utf-8-sig").read().splitlines()
    start = next(i for i, l in enumerate(lines) if l.startswith("Grünes LW-Teil;"))
    out = {}
    for r in csv.DictReader(lines[start:], delimiter=";"):
        if not r.get("Staub/Teil"):
            break
        y = {r["Staub"]: num(r["Staub/Teil"]), r["Essenz"]: num(r["Essenz/Teil"])}
        if r["Splitter"] not in ("", "–"):
            y[r["Splitter"]] = num(r["Splitter/Teil"])
        out[r["Grünes LW-Teil"]] = y
    return out


def recipes():
    return {r["rezept"]: r for r in read(os.path.join(D, "kombi", "rezepte.csv"))}


def lehrer():
    """Rezept (englisch) -> {kosten (Silber), ab (Fertigkeit), lehrer, deutsch}; dazu die Ränge («LW Lehrling» usw.).
    Zuordnung über die Item-ID (LW) oder den deutschen Namen aus rezepte_de.csv (VZ)."""
    rows = read(os.path.join(D, "kombi", "lehrer.csv"))
    de = {r["rezept_en"]: r for r in read(os.path.join(D, "kombi", "rezepte_de.csv"))}
    item_en = {r["item_id"]: n for n, r in IT.items() if r.get("item_id")}
    out = {}
    for r in rows:
        kosten = num(r["kosten_kupfer"]) / 100 if r["kosten_kupfer"] else 0.0
        e = {"kosten": kosten, "ab": num(r["ab_fertigkeit"]) if r["ab_fertigkeit"] else 0, "lehrer": r["lehrer"],
             "deutsch": r["eintrag"], "quelle": r["quelle"]}
        kurz = {"Lederverarbeitung": "LW", "Verzauberkunst": "VZ"}.get(r["beruf"])
        if r["rang"] == "ja" and kurz:
            rang = "Lehrling" if "lehrling" in r["eintrag"].lower() else "Geselle" if "geselle" in r["eintrag"].lower() else r["eintrag"]
            out.setdefault(f"{kurz} {rang}", e)
            continue
        en = item_en.get(r["item_id"]) or next((k for k, v in de.items() if v["deutsch"] == r["eintrag"]), None) or r["rezept_en"]
        if en:
            out.setdefault(en, e)
    return out, de


def ankauf():
    """Rezept/Material (englisch) -> (Silber pro Stück, Quelle), was der Händler zahlt: Forever-Client (Testlog), sonst
    die Spalte «Händlerpreis (s)» aus Kreislauf.csv (AHledger) für die grünen LW-Teile."""
    out = {}
    lines = open(os.path.join(D, "rechnung", "Kreislauf.csv"), encoding="utf-8-sig").read().splitlines()
    start = next(i for i, l in enumerate(lines) if l.startswith("Grünes LW-Teil;"))
    for r in csv.DictReader(lines[start:], delimiter=";"):
        if not r.get("Staub/Teil"):
            break
        if r.get("Händlerpreis (s)"):
            out[r["Grünes LW-Teil"]] = (num(r["Händlerpreis (s)"]), "AHledger (Kreislauf.csv), im Spiel ungeprüft")
    pfad = os.path.join(D, "preise", "haendler_ankauf.csv")
    if os.path.exists(pfad):
        by_id = {r["item_id"]: r for r in read(pfad)}
        for n, r in IT.items():
            a = by_id.get(r.get("item_id"))
            if a and a["ankauf_kupfer"]:
                out[n] = (num(a["ankauf_kupfer"]) / 100, f"Forever-Client ({a['quelle'].split(',')[0]}, {a['gemessen']})")
    return out


def segments(rows):
    """Route-Zeilen zu Abschnitten: [(von, bis, rezept, herstellungen, {material: je}, ergebnis, quelle)] bis pm.ZIEL."""
    seg = {}
    for r in rows:
        key = (num(r["von"]), num(r["bis"]), r["rezept"])
        s = seg.setdefault(key, {"n": pm.crafts_of(r), "mats": {}, "erg": r["ergebnis"], "quelle": r["quelle"]})
        s["mats"][r["material"]] = num(r["menge_je"])
    out = [(k[0], min(k[1], pm.ZIEL), k[2], v["n"], v["mats"], v["erg"], v["quelle"]) for k, v in seg.items() if v["n"] > 0]
    return sorted(out, key=lambda s: (s[0], s[1]))


def add(d, k, v):
    d[k] = d.get(k, 0.0) + v


def cost(bag, p):
    return sum(q * p.get(m, 0.0) for m, q in bag.items())


# --- Eingaben ---------------------------------------------------------------------------------------------------------
IT = items()
P, P30, VENDOR = prices()
DE = de_table()
REZ = recipes()
LEHRER, REZ_DE = lehrer()
ANKAUF = ankauf()
# Grüne Teile, die der Händler höher bezahlt, als ihr Entzauberungs-Ertrag im AH kostet: verkaufen statt entzaubern
# (Preisregel, Abschnitt 6; die Verzauberkunst kauft das fehlende Material dann im AH)
VERKAUFEN = {t for t in DE if t in ANKAUF and ANKAUF[t][0] > cost(DE[t], P)}
low, high = pm.state[pm.WECHSEL][2], pm.state[pm.WECHSEL][3]          # Plan beim Wechsel: untere und obere Rate
base = pm.state[pm.WECHSEL][0]
before_s1 = pm.before_stop["D"]                                         # Bestand vor dem Farm-Stopp S1 (Abschnitt D)
OWN = {"Light Leather": low["leder"], "Ruined Leather Scraps": low["fetzen"], "Light Hide": low["lhaut"],
       "Medium Leather": low["mleder"], "Medium Hide": low["mhaut"]}

wp = {v: pm.lw[f"wow-professions ({v})"]["rows"] for v in ("Cured Heavy Hide", "ohne Heavy Hide")}
vz_rows = [r for r in pm.need_rows if r["beruf"] == "VZ" and r["route"].startswith("wow-professions")]


# --- Lederverarbeitung: Stufen A-D mit eigenem Material zuerst ---------------------------------------------------------
def lw_plan(rows, own):
    """Simuliert LW 1-150 in den Stufen A-D. Eigenes Material zuerst, der Rest wird gekauft (auch fehlende Fetzen; ob das billiger
    ist als Light Armor Kits aus Leder, zeigt die Preisregel in Abschnitt 6 des Berichts). Entzauberte Teile zieht erst run() ab."""
    inv = dict(own)
    plan = []
    segs = segments(rows)
    for stufe, lw_bis, _, _ in STUFEN:
        lo = 0 if not plan else plan[-1]["bis"]
        part = [s for s in segs if lo <= s[0] < lw_bis]
        buy, made, steps = {}, {}, []
        for von, bis, rez, n, mats, erg, quelle in part:
            use = {}
            for m, q in mats.items():
                need = n * q
                take = min(inv.get(m, 0.0), need)
                inv[m] = inv.get(m, 0.0) - take
                use[m] = (need, take)
                if need - take > 1e-9:
                    add(buy, m, need - take)
            if erg:
                add(inv, erg, n)
                add(made, erg, n)
            steps.append({"von": von, "bis": bis, "rezept": rez, "n": n, "use": use, "quelle": quelle})
        plan.append({"stufe": stufe, "bis": lw_bis, "steps": steps, "buy": buy, "made": made, "inv": dict(inv)})
    return plan


def de_after(plan_stage, inv, keep_flb):
    """Was nach einer Stufe entzaubert wird (Teile, die die Route nicht mehr braucht) und was es ergibt; Teile aus
    VERKAUFEN gehen stattdessen an den Händler (dritter Rückgabewert)."""
    out, parts, sold = {}, {}, {}
    for item in DE:
        have = inv.get(item, 0.0)
        if item == "Fine Leather Belt":
            have = max(0.0, have - keep_flb)
        if have > 1e-9:
            inv[item] = inv.get(item, 0.0) - have
            if item in VERKAUFEN:
                sold[item] = have
                continue
            parts[item] = have
            for m, q in DE[item].items():
                add(out, m, have * q)
    return parts, out, sold


def run(variant):
    plan = lw_plan(wp[variant], OWN)
    # Entzaubern nach jeder Stufe; Fine Leather Belts für Dark Leather Belt aufheben, solange Stufe C noch kommt
    inv = {}
    de_parts, de_out, de_sold = [], [], []
    for st in plan:
        for k, v in st["made"].items():
            add(inv, k, v)
        for step in st["steps"]:
            for m, (need, take) in step["use"].items():
                if m in DE or m in ("Fine Leather Belt",):
                    inv[m] = inv.get(m, 0.0) - need
        keep = FLB_BEHALTEN if st["stufe"] in ("A", "B") else 0.0
        parts, out, sold = de_after(st, inv, keep)
        de_parts.append(parts)
        de_out.append(out)
        de_sold.append(sold)
    return plan, de_parts, de_out, de_sold


# --- Verzauberkunst: pro Fertigkeitspunkt die billigste Möglichkeit, eigenes Material zuerst --------------------------
def vz_options(staebe=False):
    """{(von, bis): [{rezept, n, mats, zurueck}]} aus den wow-professions-Wegen (Staub, Essenz, Alternative); mit staebe
    zusätzlich die Zauberstäbe aus STAEBE (je Herstellung ein Punkt, zurück = Händlerpreis), geteilt an den Grenzen der Route."""
    seg = {}
    for r in vz_rows:
        k = (num(r["von"]), num(r["bis"]))
        opt = seg.setdefault(k, {}).setdefault(r["rezept"], {"rezept": r["rezept"], "n": num(r["anzahl"]), "mats": {},
                                                               "routes": set(), "zurueck": 0.0})
        opt["mats"][r["material"]] = num(r["menge_je"])
        opt["routes"].add(r["route"])
    if staebe:
        for rez, von, bis, mats in STAEBE:
            back = ANKAUF.get(rez, (0.0, ""))[0]
            for (a, b), opts in seg.items():
                lo, hi = max(a, von), min(b, bis)
                if any("Rod" in r for r in opts):
                    continue   # Runenverzierte Ruten sind Pflicht (Werkzeug), kein Zauberstab statt ihrer
                if lo < hi:
                    opts[rez] = {"rezept": rez, "n": float(b - a), "mats": dict(mats), "routes": {"Zauberstab"},
                                 "zurueck": back, "nur": (lo, hi)}
    return {k: list(v.values()) for k, v in sorted(seg.items())}


def learn_at(rezept):
    """Ab welcher Fertigkeit das Rezept geht: Lehrerliste (gemessen), sonst «orange» laut AHledger (rezepte.csv), sonst 0."""
    e = LEHRER.get(rezept)
    if e and e["ab"]:
        return e["ab"]
    z = REZ.get(rezept)
    return num(z["orange"]) if z and z.get("orange") else 0


FORMEL = {"Enchant 2H Weapon - Lesser Intellect": "Formula: Enchant 2H Weapon - Lesser Intellect"}


def vz_plan(de_out, prices_now, staebe=False):
    """Geht VZ 1-150 Punkt für Punkt durch; nimmt pro Punkt das Rezept mit den geringsten Kaufkosten (eigenes Material kostet 0;
    was der Händler für das Ergebnis zahlt, zählt ab). Nur Rezepte, die bei diesem Punkt schon gehen (learn_at).
    Greater Magic Essence zählt als 3 Lesser (wow-professions: Rechtsklick teilt sie)."""
    opts = vz_options(staebe)
    stock = {}
    plan, formel_gekauft = [], set()
    for i, (stufe, _, vz_bis, _) in enumerate(STUFEN):
        for m, q in de_out[i].items():
            if m == "Greater Magic Essence":
                add(stock, "Lesser Magic Essence", 3 * q)
            else:
                add(stock, m, q)
        lo = 0 if not plan else plan[-1]["bis"]
        lo = max(lo, 1)
        buy, used, zur = {}, {}, 0.0
        for (von, bis), olist in opts.items():
            a, b = max(von, lo), min(bis, vz_bis)
            if a >= b:
                continue
            pts = bis - von
            for k_pt in range(int(round(b - a))):
                punkt = a + k_pt
                best, best_key = None, None
                frei = [o for o in olist if learn_at(o["rezept"]) <= punkt and o.get("nur", (0, 999))[0] <= punkt < o.get("nur", (0, 999))[1]]
                for o in (frei or olist):
                    c, own_val = 0.0, 0.0
                    for m, q in o["mats"].items():
                        need = o["n"] * q / pts
                        have = min(stock.get(m, 0.0), need)
                        c += (need - have) * prices_now.get(m, 0.0)
                        own_val += have * prices_now.get(m, 0.0)
                    f = FORMEL.get(o["rezept"])
                    if f and f not in formel_gekauft:
                        c += prices_now.get(f, 0.0)                     # Formel voll beim ersten Einsatz
                    c -= o.get("zurueck", 0.0) * o["n"] / pts           # Händler zahlt für das Ergebnis (Zauberstäbe)
                    key = (round(c, 6), round(own_val, 6))              # zuerst Kaufkosten, dann das billigere eigene Material verbrauchen
                    if best is None or key < best_key:
                        best, best_key = o, key
                for m, q in best["mats"].items():
                    need = best["n"] * q / pts
                    take = min(stock.get(m, 0.0), need)
                    stock[m] = stock.get(m, 0.0) - take
                    if need - take > 1e-9:
                        add(buy, m, need - take)
                key = (a, b, best["rezept"])                     # Bereich dieser Stufe, nicht der ganze Abschnitt der Route
                add(used, key, best["n"] / pts)
                zur += best.get("zurueck", 0.0) * best["n"] / pts
                f = FORMEL.get(best["rezept"])
                if f and f not in formel_gekauft:
                    formel_gekauft.add(f)
                    add(buy, f, 1)
        plan.append({"stufe": stufe, "bis": vz_bis, "buy": buy, "used": used, "stock": dict(stock), "zurueck": zur})
    return plan


def ceil_bag(bag):
    """Kaufmengen auf ganze Stück aufgerundet (so stehen sie im Guide)."""
    return {m: math.ceil(q - 1e-6) for m, q in bag.items() if q > 1e-6}


def tier_costs(lw, vz, de_out, p):
    rows = []
    for i, st in enumerate(lw):
        bag = dict(st["buy"])
        for m, q in vz[i]["buy"].items():
            add(bag, m, q)
        bag = ceil_bag(bag)
        rows.append((st["stufe"], bag, cost(bag, p)))
    return rows


def scan_preise():
    """Preise «jetzt» mit den Medianen des letzten eigenen AH-Scans (data/preise/ah_eigen.csv, nur zum Vergleich im Bericht;
    ob die eigenen Scans den Plan ersetzen, ist offene Entscheidung 17). Händlerware bleibt beim Händlerpreis."""
    pfad = os.path.join(D, "preise", "ah_eigen.csv")
    if not os.path.exists(pfad):
        return None, None
    rows = [r for r in read(pfad) if r.get("median_s") and r.get("hinweis", "") != "unvollständig"]
    if not rows:
        return None, None
    letzt = max(r["datum"] for r in rows)
    by_id = {r["item_id"]: num(r["median_s"]) for r in rows if r["datum"] == letzt}
    out = dict(P)
    for n, r in IT.items():
        if n not in VENDOR and r.get("item_id") in by_id:
            out[n] = by_id[r["item_id"]]
    return out, f"{letzt}, {rows[0]['markt']}"


def lehrer_stufen(lw, vz):
    """Pro Stufe: was beim Lehrer zu lernen ist (Ränge und Rezepte der Route) mit Kosten in Silber (lehrer.csv).
    Rezepte ohne Eintrag in der Liste (z. B. mit dem Rang gelernt) kosten 0; die Formel 2H Weapon steht beim Einkauf."""
    gelernt, out = set(), []
    for i, st in enumerate(lw):
        posten = []
        if i == 0:
            posten += ["LW Lehrling", "VZ Lehrling", "LW Geselle", "VZ Geselle"]
        posten += [s["rezept"] for s in st["steps"]]
        posten += [rez for (_, _, rez) in sorted(vz[i]["used"])]
        liste = []
        for p_ in posten:
            if p_ in gelernt:
                continue
            gelernt.add(p_)
            e = LEHRER.get(p_)
            if e and e["kosten"]:
                liste.append((p_, e))
        out.append(liste)
    return out


def haendler_stufen(de_sold, vz):
    """Pro Stufe: Einnahmen beim Händler für verkaufte LW-Teile (VERKAUFEN) und für Zauberstäbe (nur in der Variante)."""
    out = []
    for i, sold in enumerate(de_sold):
        v = sum(q * ANKAUF[t][0] for t, q in sold.items())
        out.append(v + vz[i].get("zurueck", 0.0))
    return out


# --- Rechnen ------------------------------------------------------------------------------------------------------------
results = {}
for variant in wp:
    lw, de_parts, de_out, de_sold = run(variant)
    vz = vz_plan(de_out, P)
    gross = sum(c for _, _, c in tier_costs(lw, vz, de_out, P))
    left = vz[-1]["stock"]
    resale = sum(max(0.0, q) * P.get(m, 0.0) for m, q in left.items())
    haendler = sum(haendler_stufen(de_sold, vz))
    results[variant] = {"lw": lw, "de_parts": de_parts, "de_out": de_out, "de_sold": de_sold, "vz": vz, "gross": gross,
                        "resale": resale, "haendler": haendler}
CHOICE = min(results, key=lambda v: results[v]["gross"] - results[v]["resale"] - results[v]["haendler"])
R = results[CHOICE]
R["lehrer"] = lehrer_stufen(R["lw"], R["vz"])
# Variante mit Zauberstäben (Vorschlag, nicht im Guide): gleiche LW-Stufen, VZ mit STAEBE
R_STAB = {"vz": vz_plan(R["de_out"], P, staebe=True)}
R_STAB["lehrer"] = lehrer_stufen(R["lw"], R_STAB["vz"])
P_SCAN, SCAN_STAND = scan_preise()


def stufen_netto(vz, lehr, p=None):
    """Pro Stufe (Einkauf, Lehrer, Händler zurück, netto) in Silber; Einkauf mit den Preisen p (Standard «jetzt»)."""
    p = p or P
    t = tier_costs(R["lw"], vz, R["de_out"], p)
    h = haendler_stufen(R["de_sold"], vz)
    out = []
    for i, (st, _, c) in enumerate(t):
        l_ = sum(e["kosten"] for _, e in lehr[i])
        out.append((st, c, l_, h[i], c + l_ - h[i]))
    return out


def sweetspot():
    """LW 1-80 (Stufe A) aus eigenem Material: was die Route braucht und was beim Wechsel da ist."""
    a = R["lw"][0]
    need = {}
    for step in a["steps"]:
        for m, (n, _) in step["use"].items():
            add(need, m, n)
    made_ll = sum(s["n"] for s in a["steps"] if s["rezept"] == "Light Leather")
    return need, made_ll


NEED_A, MADE_LL = sweetspot()
LL_NET_A = NEED_A.get("Light Leather", 0.0) - MADE_LL            # eigenes Leichtes Leder, wenn alle Fetzen da sind


def ll_points():
    """Fertigkeitspunkte je Leichtem Leder und Kosten je Punkt pro LW-Abschnitt (Plan-Variante)."""
    out = []
    for st in R["lw"]:
        for s in st["steps"]:
            pts = s["bis"] - s["von"]
            ll = s["use"].get("Light Leather", (0.0, 0.0))[0]
            mats = {m: n for m, (n, _) in s["use"].items()}
            c = cost(mats, P)
            if s["rezept"] in DE:                      # wird entzaubert (Fine Leather Belt: ohne die behaltenen)
                n_de = s["n"] - (FLB_BEHALTEN if s["rezept"] == "Fine Leather Belt" else 0)
                back = n_de * cost(DE[s["rezept"]], P)
            else:                                      # Material für später oder zum Verkauf (ohne AH-Preis: 0)
                back = s["n"] * P.get(s["rezept"], 0.0)
            out.append((st["stufe"], s, pts, ll, c, back))
    return out


def ratio():
    """Wie viel weniger Punkte je Leichtem Leder nach Stufe A als in Stufe A (kleinstes und grösstes Verhältnis)."""
    a = [pts / ll for st, s, pts, ll, c, b in ll_points() if st == "A" and ll > 0]
    later = [pts / ll for st, s, pts, ll, c, b in ll_points() if st != "A" and ll > 0]
    return min(a) / max(later), max(a) / min(later)


def skin_value(band, p):
    return sum(num(band[k]) * p.get(m, 0.0) for k, m in (("leder", "Light Leather"), ("fetzen", "Ruined Leather Scraps"),
                                                          ("lhaut", "Light Hide"), ("mleder", "Medium Leather"), ("mhaut", "Medium Hide")))


def name(m):
    r = IT.get(m)
    return f"{m} ({r['deutsch']})" if r and r["deutsch"] else m


def anzahl(n):
    return f"{n:.0f}" if abs(n - round(n)) < 0.05 else f"{n:.1f}"


def fmt_bag(bag, digits=0):
    parts = []
    for m, q in sorted(bag.items(), key=lambda kv: -kv[1] * P.get(kv[0], 0.0)):
        if q > 1e-6:
            parts.append(f"{math.ceil(q - 1e-6) if digits == 0 else round(q, digits)} {m}")
    return ", ".join(parts) or "–"


def check_learn():
    """Widersprüche zwischen den Abschnitten der Route und den Lernstufen laut AHledger (orange = lernbar ab)."""
    out = []
    for r in pm.need_rows:
        if not r["route"].startswith("wow-professions"):
            continue
        z = REZ.get(r["rezept"])
        if not z or not z["orange"]:
            continue
        if num(r["von"]) < num(z["orange"]):
            out.append((r["beruf"], r["rezept"], r["von"], z["orange"], z["quelle"]))
    return sorted(set(out))


def regeln():
    """Break-even-Regeln: (Wahl, Regel, f(Preise) -> Text mit Vergleich und Ergebnis)."""
    def cmp(a, b, ja, nein):
        return f"{silber(a)} gegen {silber(b)}: {ja if a < b else nein}"
    b2 = pm.band_of(13)
    fish = ANGELN_FAENGE_H * DEVIATE_ANTEIL
    return [
        ("Fehlende Fetzen", "kaufen, wenn 3 Fetzen weniger kosten als 2 Leichtes Leder; sonst Light Armor Kit (1 Leder)",
         lambda p: cmp(3 * p["Ruined Leather Scraps"], 2 * p["Light Leather"], "Fetzen kaufen", "Light Armor Kit")),
        ("Extra Embossed Leather Gloves nur zum Entzaubern", "lohnt, wenn 1,125 Strange Dust und 0,3 Lesser Magic Essence (Ertrag) mehr wert sind als 3 Leichtes Leder und 2 Coarse Thread",
         lambda p: cmp(3 * p["Light Leather"] + 2 * p["Coarse Thread"], 1.125 * p["Strange Dust"] + 0.3 * p["Lesser Magic Essence"],
                       "lohnt", "lohnt nicht, Staub kaufen")),
        ("VZ 20–70 und 100–109", "1 Strange Dust oder 1 Lesser Magic Essence pro Punkt: das billigere",
         lambda p: cmp(p["Lesser Magic Essence"], p["Strange Dust"], "Essenz", "Staub")),
        ("VZ 70–100", "Essenz (33 für 30 Punkte) lohnt, solange sie weniger als 1,82 Strange Dust kostet",
         lambda p: cmp(p["Lesser Magic Essence"], 60 / 33 * p["Strange Dust"], "Essenz (Chest - Minor Absorption)", "Staub (Bracer - Minor Stamina)")),
        ("VZ 110–130", "Essenz (80, dazu Formel 5s) statt 64 Strange Dust lohnt unter etwa 0,8 Strange Dust pro Essenz",
         lambda p: cmp(80 * p["Lesser Magic Essence"] + p.get("Formula: Enchant 2H Weapon - Lesser Intellect", 0.0), 64 * p["Strange Dust"],
                       "Essenz (2H Weapon - Lesser Intellect)", "Staub (Cloak - Minor Protection)")),
        ("VZ 130–150", "Soul Dust (20) statt 80 Strange Dust lohnt unter 4 Strange Dust pro Soul Dust; eigener Soul Dust aus Hillman's zählt 0",
         lambda p: cmp(20 * p["Soul Dust"], 80 * p["Strange Dust"], "Soul Dust kaufen", "Staub kaufen")),
        ("LW 130–150", "Tab «Cured Heavy Hide» (20 Heavy Hide, 60 Salt, 14 Hillman's) statt «ohne Heavy Hide» (24 Hillman's), ohne Entzaubern gerechnet",
         lambda p: cmp(20 * p["Heavy Hide"] + 60 * p["Salt"] + 14 * (14 * p["Medium Leather"] + 4 * p["Fine Thread"]),
                       24 * (14 * p["Medium Leather"] + 4 * p["Fine Thread"]), "Cured Heavy Hide", "ohne Heavy Hide")),
        ("Light Leather Pants: Händler statt Entzaubern", f"Händler zahlt {silber(ANKAUF.get('Light Leather Pants', (0, ''))[0])} (Forever-Client); lohnt, solange der Ertrag (1,875 Strange Dust, 0,3 Greater Magic Essence, 0,04 Splitter) weniger wert ist",
         lambda p: cmp(cost(DE["Light Leather Pants"], p), ANKAUF.get("Light Leather Pants", (0, ""))[0], "Händler", "entzaubern")),
        ("Dark Leather Belt: Händler statt Entzaubern", f"Händler zahlt {silber(ANKAUF.get('Dark Leather Belt', (0, ''))[0])} (Forever-Client); lohnt, solange 3,75 Strange Dust, 0,3 Lesser Astral Essence und 0,04 Splitter weniger wert sind",
         lambda p: cmp(cost(DE["Dark Leather Belt"], p), ANKAUF.get("Dark Leather Belt", (0, ""))[0], "Händler", "entzaubern")),
        ("VZ 10–75: Geringer Magiezauberstab", "statt 1 Strange Dust pro Punkt (Chest - Inferior Stamina): 1 Simple Wood und 1 Lesser Magic Essence, der Händler zahlt den Stab zurück",
         lambda p: cmp(p["Simple Wood"] + p["Lesser Magic Essence"] - ANKAUF.get("Lesser Magic Wand", (0, ""))[0], p["Strange Dust"], "Zauberstab", "Staub")),
        ("VZ 70–110: Grosser Magiezauberstab", "statt 2 Strange Dust (Bracer - Minor Stamina): 1 Simple Wood und 2 Lesser Magic Essence, der Händler zahlt den Stab zurück",
         lambda p: cmp(p["Simple Wood"] + 2 * p["Lesser Magic Essence"] - ANKAUF.get("Greater Magic Wand", (0, ""))[0], 2 * p["Strange Dust"], "Zauberstab", "Staub")),
        ("Leder grinden statt angeln", "Grinden (50–80 Häute pro Stunde, Gegner 11–15) bringt mehr als Angeln (nur Deviate Fish, Rate ungeprüft)",
         lambda p: f"{silber(50 * skin_value(b2, p))}–{silber(80 * skin_value(b2, p))} gegen {silber(fish * p['Deviate Fish'])} pro Stunde: "
                   + ("Grinden" if 80 * skin_value(b2, p) > fish * p["Deviate Fish"] else "Angeln")),
    ]


RATIO = None


# --- Bericht ------------------------------------------------------------------------------------------------------------
def main(OUT):
    global RATIO
    RATIO = ratio()
    lw, vz, de_parts, de_out = R["lw"], R["vz"], R["de_parts"], R["de_out"]
    b2, b3 = pm.band_of(13), pm.band_of(18)
    L = ["# Berufe-Plan: Wechsel in Orgrimmar, Lederverarbeitung und Verzauberkunst bis 150 (erzeugt von `tools/plan_berufe.py`)", "",
         "Nicht von Hand ändern: Eingaben anpassen (Preise, Route, Modell) und neu erzeugen. Zum Start mit den Preisen des eigenen Realms neu rechnen.", "",
         "## Quellen", "",
         "- Lederverarbeitung 1–155: wow-professions, Leatherworking Leveling Guide (Forever-Beta, «still in progress»), abgerufen 14.10.2026 https://www.wow-professions.com/forever/leatherworking-leveling-guide",
         "- Verzauberkunst 1–150: wow-professions, Enchanting Leveling Guide (Forever-Beta), abgerufen 14.10.2026 https://www.wow-professions.com/forever/enchanting-leveling-guide · Entzaubern ab Fertigkeit 1: https://www.wow-professions.com/forever/disenchanting-guide",
         "- Lernstufen und Farben der Rezepte: AHledger, Rezeptseiten (Forever-Beta) https://ahledger.com/wow-forever/professions/leatherworking · https://ahledger.com/wow-forever/professions/enchanting · SeeMeta https://seemeta.com/en/wow-forever/professions/enchanting",
         "- Lehrer und Händler in Orgrimmar: Icy Veins https://www.icy-veins.com/wow-forever/leatherworking · https://www.icy-veins.com/wow-forever/enchanting · kami-labs https://kami-labs.fr/en/guide-enchantement-wow-forever/ · AHledger NPC-Seiten Kithas https://ahledger.com/wow-forever/npcs/3346-kithas und Tamar https://ahledger.com/wow-forever/npcs/3366-tamar · RXP v4.11.23 (Kamari, Auctioneer Thathung)",
         "- Preise: AHledger, Forever-Beta, Normal Horde US (`data/rechnung/Preise.csv`, Stand der Seiten 27.09.–12.10.; `data/kombi/preise_zusatz.csv`). EU-Preise gibt es erst zum Start.",
         "- Entzaubern (Erwartungswert pro Teil): `data/rechnung/Kreislauf.csv` nach der Tabelle von wow-professions.",
         "- Eigener Bestand beim Wechsel: Mengenmodell `docs/plan/mengen-leder.md` (`tools/plan_mengen.py`).",
         "- Fischen: AHledger, Item 6522 Deviate Fish (Lushwater Oasis 35 % von 153 Fängen; Median Normal Horde US 4s 50c, PvP Horde US 10s 99c) https://ahledger.com/items/6522-deviate-fish · Fangrate: Testlog 13.10. (Stonebull Lake).", ""]
    own = eigene_preise()
    if own:   # seit Testlog 3.5: eigene AH-Scans ersetzen den Preis «jetzt» (die 30-Tage-Werte bleiben AHledger)
        L.insert(-1, f"- Eigene AH-Scans (`tools/ah_aus_testlog.py --eintragen`, Bericht `docs/plan/ah-preise.md`) für {len(own)} Materialien: "
                     "«jetzt» = 7-Tage-Median der eigenen Scans; die 30-Tage-Werte bleiben AHledger. " + ", ".join(sorted(own)) + ".")

    # Ergebnis kurz
    t = {s: c for s, _, c in tier_costs(lw, vz, de_out, P)}
    t30 = {s: c for s, _, c in tier_costs(lw, vz, de_out, P30)}
    L += ["## Ergebnis in Kürze", "",
          f"- **Sweetspot** für das eigene Leder (Lesart von Claude, Abschnitt 1): Lederverarbeitung 1–80 (Stufe A). Dafür braucht es {NEED_A.get('Ruined Leather Scraps', 0):.0f} Fetzen, "
          f"{LL_NET_A:.0f} Leichtes Leder (dazu {MADE_LL:.0f} aus den Fetzen) und {NEED_A.get('Light Hide', 0):.0f} Light Hide.",
          f"- Laut Modell bringt die Route bis Orgrimmar {before_s1['leder']:.0f} Leichtes Leder und {before_s1['fetzen']:.0f} Fetzen, mit dem Grinden auf Stufe 16 "
          f"an Raptoren (Farm-Stopp S1, RXP schlägt das Grinden dort ohnehin vor) {low['leder']:.0f}–{high['leder']:.0f} und {low['fetzen']:.0f}–{high['fetzen']:.0f}. "
          f"Laut Modell reicht das Leder; die fehlenden Fetzen und Bälge kosten im AH wenig (Stufe A unten).",
          f"- Ab LW 80 bringt jedes Leichte Leder {RATIO[0]:.0f}- bis {RATIO[1]:.0f}-mal weniger Punkte als davor (Tabelle in Abschnitt 1). Mehr Leder zu farmen bringt "
          f"{50 * skin_value(b2, P):.0f}–{80 * skin_value(b2, P):.0f} Silber pro Stunde Materialwert (Beta); Angeln ergäbe etwa {silber(ANGELN_FAENGE_H * DEVIATE_ANTEIL * P['Deviate Fish'])} pro Stunde (nur Deviate Fish, Rate ungeprüft, Abschnitt 1).",
          f"- Einkauf (Beta-Preise «jetzt»): Stufe A {silber(t['A'])}, B {silber(t['B'])}, C {silber(t['C'])}, D {silber(t['D'])}. "
          f"Derselbe Einkauf mit den 30-Tage-Medianen: A {silber(t30['A'])}, B {silber(t30['B'])}, C {silber(t30['C'])}, D {silber(t30['D'])}.",
          "- Mit Lehrer (Lernkosten gemessen in Orgrimmar, `data/kombi/lehrer.csv`) und dem, was der Händler für verkaufte Teile zahlt: "
          + ", ".join(f"Stufe {st} {silber(c)} + Lehrer {silber(l_)} − Händler {silber(h)} = netto {silber(n)}" for st, c, l_, h, n in stufen_netto(vz, R["lehrer"]))
          + f". Zusammen netto {silber(sum(x[4] for x in stufen_netto(vz, R['lehrer'])))}.",
          (f"- Derselbe Plan mit den Medianen des letzten eigenen AH-Scans ({SCAN_STAND}; nur Vergleich, offene Entscheidung 17): "
           + ", ".join(f"{st} netto {silber(n)}" for st, c, l_, h, n in stufen_netto(vz, R["lehrer"], P_SCAN))
           + f", zusammen {silber(sum(x[4] for x in stufen_netto(vz, R['lehrer'], P_SCAN)))}." if P_SCAN else
           "- Eigene AH-Scans: noch keine in `data/preise/ah_eigen.csv`."),
          f"- Verkaufen statt entzaubern (Preisregel, Abschnitt 6): {', '.join(sorted(t_ for t_ in VERKAUFEN if any(t_ in sold for sold in R['de_sold'])))} "
          "gehen an den Händler, weil er mehr zahlt, als ihr Entzauberungs-Ertrag im AH kostet (Händlerpreise aus dem Forever-Client, Testlog 15.10.).",
          f"- Vorschlag (nicht im Guide, Abschnitt 9): VZ 10–109 mit Zauberstäben, die der Händler zurückkauft. Netto A–D zusammen "
          f"{silber(sum(x[4] for x in stufen_netto(R_STAB['vz'], R_STAB['lehrer'])))} statt {silber(sum(x[4] for x in stufen_netto(vz, R['lehrer'])))}.",
          f"- LW 130–150 rechnet der Plan mit dem Tab «{CHOICE}» von wow-professions (billiger bei diesen Preisen, Vergleich in Abschnitt 4).",
          f"- Nach allen Stufen bleibt Entzauberungs-Material übrig, das VZ bis 150 nicht braucht (Wert im AH etwa {silber(R['resale'])}, Abschnitt 5).", ""]

    # 1. Sweetspot
    L += ["## 1. Sweetspot: wie viel eigenes Leder nach Orgrimmar", "",
          "Lesart von Claude (Rückfrage an den Nutzer offen): «Break-even an Investment von leichtem Leder» heisst hier: eigenes Leder dort einsetzen, wo es "
          "viele Punkte bringt, und nur so viel sammeln, wie die Route ohnehin hergibt (plus das Grinden, das RXP selbst vorschlägt). Bei Beta-Preisen "
          "ist Kaufen billiger als zusätzliches Farmen (Rechnung unten); bei anderen Preisen kann das kippen.", "",
          "| Material | LW 1–80 braucht | Route bis Orgrimmar (ohne S1) | mit S1 (untere–obere Rate) | im AH kaufen (mit S1, untere Rate) | Beta-Preis |",
          "|---|---|---|---|---|---|"]
    for m, key in (("Ruined Leather Scraps", "fetzen"), ("Light Leather", "leder"), ("Light Hide", "lhaut")):
        need = LL_NET_A if m == "Light Leather" else NEED_A.get(m, 0.0)
        buy = max(0.0, need - low[key])
        L.append(f"| {name(m)} | {need:.0f}{' (netto; ' + format(MADE_LL, '.0f') + ' mehr entstehen aus den Fetzen)' if m == 'Light Leather' else ''} | "
                 f"{before_s1[key]:.0f} | {low[key]:.0f}–{high[key]:.0f} | {buy:.0f} | {silber(P[m])} |")
    L += ["", f"Die {before_s1['leder']:.0f} Leder ohne S1 setzen voraus, dass die 5 Plainstrider Kidneys (Quest 821) vor Orgrimmar fallen (Annahme in "
          "`modell_leder.csv`; RXP erinnert bis 12-17 #180 daran); ohne sie wären es etwa 60. Ist der Zähler beim Farm-Stopp S1 schon voll, ist S1 nur Zugabe.",
          "", "Punkte pro Leichtem Leder und Kosten pro Punkt (Plan-Route, Beta-Preise «jetzt»; «zurück» = Wert, der als Material oder beim Entzaubern zurückkommt; "
          "netto negativ = Gewinn):", "",
          "| Stufe | LW | Rezept | Herstellungen | Leichtes Leder | Punkte je Leder | Material (AH/Händler) | zurück | netto je Punkt |", "|---|---|---|---|---|---|---|---|---|"]
    for stufe, s, pts, ll, c, back in ll_points():
        ppl = f"{pts / ll:.2f}" if ll else "–"
        L.append(f"| {stufe} | {s['von']:.0f}–{s['bis']:.0f} | {s['rezept']} | {s['n']:.0f} | {ll:.0f} | {ppl} | {silber(c)} | {silber(back)} | {silber((c - back) / pts)} |")
    fish_h = ANGELN_FAENGE_H * DEVIATE_ANTEIL
    L += ["", "Zeit gegen Gold (Beta-Preise; Raten sind Annahmen, siehe Abschnitt 8):", "",
          f"- Grinden für Leder, Gegner Stufe 11–15: {50 * skin_value(b2, P):.0f}–{80 * skin_value(b2, P):.0f} Silber pro Stunde Materialwert bei 50–80 Häuten "
          f"(30-Tage-Preise: {50 * skin_value(b2, P30):.0f}–{80 * skin_value(b2, P30):.0f}). Dazu gibt es XP; RXP schlägt das Grinden auf Stufe 16 an der Sludge Fen ohnehin vor.",
          f"- Angeln an der Lushwater Oasis, nur Deviate Fish gerechnet: rund {fish_h:.0f} pro Stunde bei der Fangrate vom Stonebull Lake ergibt "
          f"{silber(fish_h * P['Deviate Fish'])} pro Stunde (Normal Horde US) bzw. {silber(fish_h * DEVIATE_PH)} (PvP Horde US). Ungeprüft: Fangrate und "
          "nötige Angelfertigkeit im Brachland (keine Forever-Quelle).",
          f"- Folgerung (bei diesen Preisen): Grinden nur für Leder lohnt sich erst, wenn Leichtes Leder etwa "
          f"{silber(fish_h * P['Deviate Fish'] / (80 * num(b2['leder'])))}–{silber(fish_h * P['Deviate Fish'] / (50 * num(b2['leder'])))} kostet "
          f"(heute {silber(P['Light Leather'])}).", ""]

    # 2. Stufen
    L += ["## 2. Ablauf: Stufen A bis D", "",
          "Stufe A ist die Sitzung in Orgrimmar (LW 1–80, VZ 1–50, beide Gesellen). Stufe B geht dort auch, wenn das Gold reicht; C und D (und B, falls noch offen) "
          "kommen in Thunder Bluff (Route «17-22», Stufe 20). Herstellungen laut wow-professions; der Guide-Schritt endet bei der Zielfertigkeit, Rest bleibt für die nächste Stufe.", ""]
    for i, st in enumerate(lw):
        stufe, lwb, vzb, zweck = STUFEN[i]
        L += [f"### Stufe {stufe}: LW bis {lwb}, VZ bis {vzb} ({zweck})", ""]
        L += ["Herstellen (Lederverarbeitung):", ""]
        for s in st["steps"]:
            mats = ", ".join(f"{need:.0f} {m}" + (f" (davon {take:.0f} aus dem Vorrat)" if take > 0.5 else "") for m, (need, take) in s["use"].items())
            L.append(f"- LW {s['von']:.0f}→{s['bis']:.0f}: {s['n']:.0f}× {s['rezept']} — {mats}")
        sold = R["de_sold"][i]
        if sold:
            L += ["", "Beim Händler verkaufen (statt entzaubern): " + ", ".join(
                f"{q:.0f}× {m} zu je {silber(ANKAUF[m][0])} = {silber(q * ANKAUF[m][0])}" for m, q in sold.items())]
        parts = de_parts[i]
        if parts:
            L += ["", "Entzaubern: " + ", ".join(f"{q:.0f}× {m}" for m, q in parts.items()) + " → erwartet " + fmt_bag(de_out[i], 1)
                  + (f". {FLB_BEHALTEN} Fine Leather Belt behalten (für Dark Leather Belt in Stufe C)." if stufe in ("A", "B") and any(
                      s['rezept'] == 'Fine Leather Belt' for s in st['steps']) else "")]
        L += ["", "Verzaubern:", ""]
        for (von, bis, rez), n in sorted(vz[i]["used"].items()):
            L.append(f"- VZ {von:.0f}–{bis:.0f}: {anzahl(n)}× {rez}")
        bag = dict(st["buy"])
        for m, q in vz[i]["buy"].items():
            add(bag, m, q)
        bag = ceil_bag(bag)
        ah = {m: q for m, q in bag.items() if m not in VENDOR}
        ven = {m: q for m, q in bag.items() if m in VENDOR}
        lehr = R["lehrer"][i]
        L += ["", f"Einkauf im AH: {fmt_bag(ah)} = {silber(cost(ah, P))} (derselbe Einkauf mit den 30-Tage-Medianen: {silber(cost(ah, P30))})",
              f"Einkauf beim Händler: {fmt_bag(ven)} = {silber(cost(ven, P))}",
              "Beim Lehrer: " + (", ".join(f"{n_} {silber(e['kosten'])} ({e['lehrer']}, ab {e['ab']:.0f})" if e["ab"] else
                                           f"{n_} {silber(e['kosten'])} ({e['lehrer']})" for n_, e in lehr) or "–")
              + f" = {silber(sum(e['kosten'] for _, e in lehr))}", ""]

    # 3. Lernstufen
    L += ["## 3. Lernstufen: wo die Quellen sich widersprechen", "",
          "wow-professions nutzt diese Rezepte früher, als AHledger sie lernen lässt («orange» = lernbar ab). Im Spiel prüfen; der Guide nennt einen Ausweg.", "",
          "| Beruf | Rezept | wow-professions ab | AHledger lernbar ab | Quelle |", "|---|---|---|---|---|"]
    for beruf, rez, von, orange, q in check_learn():
        L.append(f"| {beruf} | {rez} | {von} | {orange} | {q} |")

    # 4. Varianten ab 130
    L += ["", "## 4. LW 130–150: Tab «Cured Heavy Hide» oder «ohne Heavy Hide»", "",
          "wow-professions: «If 20x Heavy Hide cost less than around 120x Heavy Leather, 140x Medium Leather and 17x Moss Agate» → Tab «Cured Heavy Hide», sonst "
          "«Leveling without Heavy Hide». Die Regel denkt bis 175; hier zählt nur bis 150.", "",
          "| Tab | Einkauf A–D (jetzt) | Rückverkauf übriges Material | netto |", "|---|---|---|---|"]
    for v, r in results.items():
        L.append(f"| {v} | {silber(r['gross'])} | {silber(r['resale'])} | {silber(r['gross'] - r['resale'])} |")
    L += ["", f"Der Plan nimmt «{CHOICE}». Bei anderen Preisen zum Start kann es kippen: neu rechnen.", ""]

    # 5. Verkauf
    left = vz[-1]["stock"]
    L += ["## 5. Verkaufen im AH", "",
          "Was nach Stufe D übrig bleibt (Erwartungswert) und nicht für VZ bis 150 gebraucht wird. Ob man es für LW oder VZ über 150 behält, entscheidest du.", "",
          "| Material | Menge | Wert (jetzt) | Wert (30 Tage) |", "|---|---|---|---|"]
    for m, q in sorted(left.items(), key=lambda kv: -kv[1] * P.get(kv[0], 0.0)):
        if q > 0.3:
            L.append(f"| {name(m)} | {q:.1f} | {silber(q * P.get(m, 0.0))} | {silber(q * P30.get(m, 0.0))} |")
    inv_end = lw[-1]["inv"]
    rest = {m: q for m, q in inv_end.items() if q > 0.3 and m not in DE and m != "Fine Leather Belt"}
    if rest:
        L += ["", "Dazu aus der Lederverarbeitung: " + ", ".join(f"{q:.0f} {m}" for m, q in rest.items()) + ". Heavy Leather braucht wow-professions erst ab LW 155."]
    L += ["", "Produkte der Verzauberkunst (Zauberstäbe): Der Forever-Client zahlt beim Händler "
          f"{silber(ANKAUF.get('Lesser Magic Wand', (0, ''))[0])} für den Geringen und {silber(ANKAUF.get('Greater Magic Wand', (0, ''))[0])} "
          "für den Grossen Magiezauberstab (Gegenstands-Infos, Testlog 15.10.; der Verkauf von 11 grossen für 22s am 14.10. passt dazu). "
          "Eine Patch-Notiz vom 01.10. nannte 1c (Widerspruch 21). Der Plan rechnet nur in der Variante von Abschnitt 9 damit; zum Start neu prüfen.", ""]

    # 6. Item-IDs
    L += ["## 6. Preisregeln (Break-even)", "",
          "Wann sich eine Wahl umdreht. Spalten: Wert mit den Beta-Preisen «jetzt» und mit den 30-Tage-Medianen (AHledger, Normal Horde US); "
          "der Plan oben rechnet mit «jetzt». Zum Start mit den eigenen Preisen prüfen.", "",
          "| Wahl | Regel | jetzt | 30 Tage |", "|---|---|---|---|"]
    for wahl, regel, f in regeln():
        L.append(f"| {wahl} | {regel} | {f(P)} | {f(P30)} |")
    L += ["", "## 7. Gegenstände im Guide (Item-IDs)", "", "| Gegenstand | deutsch (Testlog) | ID | Quelle |", "|---|---|---|---|"]
    for n_, r in IT.items():
        L.append(f"| {n_} | {r['deutsch'] or '–'} | {r['item_id']} | {r['quelle']} |")

    # 7. Annahmen
    L += ["", "## 8. Annahmen und offene Punkte", "",
          f"- Eigener Bestand: untere Rate des Mengenmodells beim Wechsel (Abschnitt {pm.WECHSEL}). Was der Zähler im Spiel zeigt, gilt.",
          "- Herstellungen pro Abschnitt: wow-professions («These numbers are estimates»). Der letzte Abschnitt bis 155 ist bis 150 anteilig gezählt.",
          f"- Fehlende Fetzen: kaufen ist billiger als Light Armor Kits aus Leder, solange 3 × Fetzenpreis < 2 × Lederpreis (heute {silber(3 * P['Ruined Leather Scraps'])} gegen {silber(2 * P['Light Leather'])}).",
          "- Entzaubern: Erwartungswert aus `Kreislauf.csv`; Greater Magic Essence zählt als 3 Lesser (wow-professions: Rechtsklick teilt sie).",
          "- Verzaubern: pro Punkt das Rezept mit den geringsten Kaufkosten; eigenes Material kostet nichts. Ob man ein Zielteil (Armschiene, Brust, Umhang, Stiefel, "
          "Zweihänder) braucht, sagt keine Forever-Quelle ausdrücklich (wow-professions erwähnt im Makro einen «optional target slot»).",
          "- Lehrer: Lernstufen und Kosten gemessen bei Kamari, Karolek, Jhag und Godan (Orgrimmar, Testlog 15.10., `data/kombi/lehrer.csv`): "
          "Lehrling 10c, Geselle 5s (ab Stufe 10 und Fertigkeit 50), Rezepte 50c bis 25s. Lehrer in Thunder Bluff nicht gemessen. Rezepte ohne Eintrag "
          "in der Liste (Light Leather, Light Armor Kit, Runed Copper Rod, Bracer - Inferior Stamina, Bracer - Minor Deflect) zählen mit 0; laut SeeMeta "
          "kommt Minor Deflect mit dem Rang (https://seemeta.com/en/wow-forever/professions/enchanting, Stand 14.10.2026), im Spiel ungeprüft.",
          "- Händler zahlt (Verkauf der Teile): Forever-Client (`data/preise/haendler_ankauf.csv`, Testlog 15.10.); für Teile ohne Messung "
          "AHledger (Spalte «Händlerpreis (s)» in `Kreislauf.csv`), im Spiel ungeprüft. Viele hergestellte Teile zahlt der Forever-Händler "
          "niedriger als Classic (z. B. Grosser Magiezauberstab 2s statt 15s 35c, Geprägte Lederhandschuhe 71c statt 1s 19c; Vergleich in "
          "`docs/recherche/2026-10-15_haendlerpreise.md`).",
          f"- Fangrate beim Angeln: {ANGELN_FAENGE_H:.0f} Fänge pro Stunde (Testlog 13.10., Stonebull Lake, Angeln 1–15: 14 Fänge, 13 Abstände in 349 s). Im Brachland ungeprüft.",
          "- Preise: Beta, Normal Horde US. Zum Start zählen die Preise des eigenen Realms (offene Entscheidung 4).", ""]

    # 9. Variante Zauberstäbe
    L += ["## 9. Variante: Verzauberkunst mit Zauberstäben (Vorschlag von Claude, nicht im Guide)", "",
          "Idee: Der Geringe Magiezauberstab (ab VZ 10, 50c beim Lehrer) ist laut SeeMeta bis VZ 75 orange, der Grosse (ab VZ 70, 2s) bis 110 "
          "(https://seemeta.com/en/wow-forever/professions/enchanting, Stand 14.10.2026; bei VZ 100 im Testlog 15.10. bestätigt: Geringer grün, "
          "Grosser orange). Orange heisst: jede Herstellung gibt einen Punkt. Der Händler kauft die Stäbe zurück (Forever-Client: "
          f"{silber(ANKAUF.get('Lesser Magic Wand', (0, ''))[0])} bzw. {silber(ANKAUF.get('Greater Magic Wand', (0, ''))[0])}). "
          "Gleiche Lederverarbeitung wie oben; die Verzauberkunst nimmt pro Punkt das Billigste, Zauberstäbe eingeschlossen.", "",
          "| Stufe | Einkauf | Lehrer | Händler zurück | netto | ohne Zauberstäbe netto |", "|---|---|---|---|---|---|"]
    base = {x[0]: x for x in stufen_netto(vz, R["lehrer"])}
    for st, c, l_, h, n in stufen_netto(R_STAB["vz"], R_STAB["lehrer"]):
        L.append(f"| {st} | {silber(c)} | {silber(l_)} | {silber(h)} | {silber(n)} | {silber(base[st][4])} |")
    L += ["", "Verzaubern in der Variante:", ""]
    for i, st in enumerate(STUFEN):
        used = R_STAB["vz"][i]["used"]
        if used:
            L.append(f"- Stufe {st[0]}: " + ", ".join(f"VZ {a:.0f}–{b:.0f} {anzahl(n)}× {rez}" for (a, b, rez), n in sorted(used.items())))
    L += ["", "Was dafür spricht und was offen ist:", "",
          "- Bei den eigenen Scan-Preisen vom 15.10. (Lesser Magic Essence 88c, Strange Dust 60c) kostet ein Punkt mit dem Geringen Stab netto "
          "etwa 16c statt 60c, mit dem Grossen etwa 14c statt 1s 20c (Regeln in Abschnitt 6).",
          "- Offen: ob die Farben in Forever so laufen (SeeMeta, nur bei VZ 100 geprüft; das Testlog schreibt jeden Farbwechsel), ob der Händlerpreis "
          "zum Start bleibt (Widerspruch 21) und ob der Markt die nötigen Essenzen hat (am 15.10. rund 2500 Stück im Angebot).",
          "- Entscheid beim Nutzer (offener Punkt 7: woher das Material für Verzauberkunst kommt).", ""]

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")

    # Konsole: Zahlen für plan.csv
    print(f"Variante ab 130: {CHOICE} | Sweetspot A: {NEED_A.get('Ruined Leather Scraps', 0):.0f} Fetzen, {LL_NET_A:.0f} LL netto, {NEED_A.get('Light Hide', 0):.0f} Light Hide")
    print(f"Bestand beim Wechsel: LL {low['leder']:.1f}-{high['leder']:.1f}, Fetzen {low['fetzen']:.1f}-{high['fetzen']:.1f}, LH {low['lhaut']:.1f} | vor S1: LL {before_s1['leder']:.1f}, Fetzen {before_s1['fetzen']:.1f}")
    for i, st in enumerate(lw):
        bag = dict(st["buy"])
        for m, q in vz[i]["buy"].items():
            add(bag, m, q)
        print(f"Stufe {st['stufe']}: kaufen {fmt_bag(bag)} = {silber(cost(bag, P))} | entzaubern {fmt_bag(de_parts[i])} -> {fmt_bag(de_out[i], 1)}"
              f" | Händler {fmt_bag(R['de_sold'][i])} | Lehrer {silber(sum(e['kosten'] for _, e in R['lehrer'][i]))}")
        for (von, bis, rez), n in sorted(vz[i]["used"].items()):
            print(f"   VZ {von:.0f}-{bis:.0f} {rez}: {n:.1f}")
    print(f"Rest: {fmt_bag(vz[-1]['stock'], 1)}")
    print(f"Bericht: {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "docs", "plan", "berufe-plan.md"))
