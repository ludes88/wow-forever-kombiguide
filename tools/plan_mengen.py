# Mengenmodell Leder bis Stufe 20: was die RXP-Route bringt, was Lederverarbeitung 150 und Verzauberkunst 150 brauchen,
# und wie gross die Lücke ist (Farmzeit oder AH-Gold).
#
# Aufruf: python3 tools/plan_mengen.py [Bericht.md]      (Standard: docs/plan/mengen-leder.md)
# Eingaben (alle mit Quelle pro Zeile):
#   data/kombi/abschnitte.csv          Abschnitte der Route mit erwarteter Stufe am Ende (aus RXPs .xp-Schritten)
#   data/kombi/modell_leder.csv        eine Zeile pro Quest mit Tieren (Anzahl aus den RXP-Kommentaren, Tauren-Druide, v4.11.23)
#   data/kombi/kuerschnern_anteile.csv Anteile Leder/Fetzen/Häute nach Gegnerstufe
#   data/kombi/farmstellen.csv         Farmstellen entlang der Route (Mitte der RXP-Schleifen)
#   data/kombi/bedarf_lw_vz.csv        Lederverarbeitung und Verzauberkunst 1-150 nach Forever-Routen
#   data/rechnung/Kreislauf.csv        Ertrag beim Entzaubern der grünen LW-Teile
#   data/rechnung/Preise.csv           AH-Rechenpreise (Beta)
#
# Rechnung pro Modellzeile: Kills = Stück × Kills je Stück; jede Haut gibt 1 Gegenstand (Testlog 13.10.), verteilt nach dem
# Band der Gegnerstufe. «Quest» zählt zur Basis; «Option: …» steht getrennt daneben.
# Als Modul (import plan_mengen) liefert die Datei nur das Modell (state, before_stop, lw, …); der Bericht entsteht nur beim Aufruf.
import csv, math, os, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

# KONSTANTEN mit Quelle
START = {"leder": 8, "fetzen": 13}          # Testlog 13.10. 22:42 (Tauren-Druide, Stufe 7, Kürschnerei 22)
ZIEL = 150                                    # Ziel Lederverarbeitung und Verzauberkunst (Entscheidung des Nutzers)
STAND_15, STAND_20 = "D", "G"                 # Abschnitt, an dessen Ende die Route Stufe 15 bzw. 20 erwartet (abschnitte.csv)
WECHSEL = "E1"                                # Berufswechsel in Orgrimmar (12-17 #92-#108, Stufe 16): danach kein eigenes Leder mehr
                                              # (Entscheidung des Nutzers 14.10., docs/entscheidungen.md)
FARM_HAEUTE_H = (50, 80)                      # Annahme, keine Quelle für Stufe 12-20; Messung Mulgore siehe Bericht
KILLS_JE_STUECK_GEMESSEN = "Quest 748 am 13.10.: 14 Wölfe für 6 Pfoten (2,3), 6 Ebenenschreiter für 4 Krallen (1,5)"
LEDER_IDS = {"Light Leather": "Leichtes Leder", "Medium Leather": "Mittleres Leder", "Ruined Leather Scraps": "Verdorbene Lederfetzen",
             "Light Hide": "Leichter Balg", "Medium Hide": "Mittlerer Balg"}
GLOVES = "Embossed Leather Gloves"            # günstigstes grünes LW-Teil zum Entzaubern (3 Leichtes Leder)


def read(path, skip=0):
    with open(path, encoding="utf-8-sig", newline="") as f:
        for _ in range(skip):
            f.readline()
        rows = list(csv.DictReader(f, delimiter=";"))
    for i, r in enumerate(rows, start=skip + 2):
        if None in r:   # mehr Felder als Spalten: meist ein Semikolon im Text
            raise SystemExit(f"{os.path.relpath(path, ROOT)} Zeile {i}: zu viele Felder (Semikolon im Text? « · » verwenden)")
    return rows


def silber(s):
    if s < 0:
        return "−" + silber(-s)
    g, r = divmod(round(s * 100), 10000)
    sv, k = divmod(r, 100)
    parts = []
    if g: parts.append(f"{g}g")
    if sv or (g and k): parts.append(f"{sv}s")   # «2g 0s 64c», nicht «2g 64c» (liest sich wie ein Tippfehler)
    if k or not parts: parts.append(f"{k}c")
    return " ".join(parts)


def num(s):
    return float(str(s).replace(",", ".")) if str(s).strip() else 0.0


# --- Eingaben ---------------------------------------------------------------------------------------------------------
D = os.path.join(ROOT, "data")
sections = read(os.path.join(D, "kombi", "abschnitte.csv"))
bands = read(os.path.join(D, "kombi", "kuerschnern_anteile.csv"))
rows = read(os.path.join(D, "kombi", "modell_leder.csv"))
spots = read(os.path.join(D, "kombi", "farmstellen.csv"))
stops = read(os.path.join(D, "kombi", "farmstopps.csv"))
need_rows = read(os.path.join(D, "kombi", "bedarf_lw_vz.csv"))
prices = {r["Material"]: num(r["Rechenpreis (s)"]) for r in read(os.path.join(D, "rechnung", "Preise.csv"), skip=1) if r.get("Material")}
kreislauf_lines = open(os.path.join(D, "rechnung", "Kreislauf.csv"), encoding="utf-8-sig").read().splitlines()
start = next(i for i, l in enumerate(kreislauf_lines) if l.startswith("Grünes LW-Teil;"))
de = {}
for r in csv.DictReader(kreislauf_lines[start:], delimiter=";"):
    if not r.get("Staub/Teil"):
        break
    de[r["Grünes LW-Teil"]] = {"staub": r["Staub"], "staub_je": num(r["Staub/Teil"]), "essenz": r["Essenz"], "essenz_je": num(r["Essenz/Teil"])}


def band_of(level):
    for b in bands:
        if int(b["stufe_von"]) <= level <= int(b["stufe_bis"]):
            return b
    raise SystemExit(f"Keine Kürschner-Anteile für Gegnerstufe {level} (data/kombi/kuerschnern_anteile.csv)")


# --- Angebot: was die Route bringt ---------------------------------------------------------------------------------------
KEYS = ["leder", "fetzen", "lhaut", "mleder", "mhaut"]
sec_ids = [s["abschnitt"] for s in sections]
quest_rows = {}
per = {sid: {"kb": 0.0, "ko": 0.0, "kf": [0.0, 0.0], "min": 0.0, "b": dict.fromkeys(KEYS, 0.0), "o": dict.fromkeys(KEYS, 0.0),
             "f": [dict.fromkeys(KEYS, 0.0), dict.fromkeys(KEYS, 0.0)],      # Farm-Stopps in diesem Abschnitt (untere, obere Rate)
             "adj": [dict.fromkeys(KEYS, 0.0), dict.fromkeys(KEYS, 0.0)]}    # Quest-Kills, die ein Farm-Stopp vorher schon erledigt
       for sid in sec_ids}
detail = []
for r in rows:
    if r["abschnitt"] not in per:
        raise SystemExit(f"Abschnitt {r['abschnitt']} fehlt in data/kombi/abschnitte.csv")
    if r["art"] == "Verbrauch":                 # Leder, das die Route verbraucht (z. B. Quest 768)
        per[r["abschnitt"]]["b"]["leder"] -= num(r["stueck"]) * num(r["kills_je_stueck"])
        detail.append((r, 0.0, "–"))
        continue
    kills = num(r["stueck"]) * num(r["kills_je_stueck"])
    b = band_of(int(num(r["kreatur_stufe"])))
    tgt = "b" if r["art"] == "Quest" else "o"
    per[r["abschnitt"]]["kb" if tgt == "b" else "ko"] += kills
    for k in KEYS:
        per[r["abschnitt"]][tgt][k] += kills * num(b[k])
    detail.append((r, kills, b["band"]))
    if tgt == "b":
        quest_rows.setdefault(r["quest"].strip(), []).append((r["abschnitt"], kills, b))
spot_by = {f["id"]: f for f in spots}
# Farm-Stopps: Kills an Tieren, die eine Quest der Route ohnehin braucht («ueberschneidet»), sind nicht zusätzlich.
# Sie werden aus dem Abschnitt der Quest herausgenommen (dort nicht mehr gezählt) und gehören zum Farm-Stopp.
for st in stops:
    if st["abschnitt"] not in per or st["farmstelle"] not in spot_by:
        raise SystemExit(f"Farm-Stopp {st['id']}: Abschnitt oder Farmstelle unbekannt")
    b = band_of(int(num(st["kreatur_stufe"])))
    p = per[st["abschnitt"]]
    p["min"] += num(st["minuten"])
    over = [(sec, kills, rb) for q in st.get("ueberschneidet", "").split(",") if q.strip() for sec, kills, rb in quest_rows.get(q.strip(), [])]
    over_kills = sum(k for _, k, _ in over)
    st["absorbiert"] = []
    for i, rate in enumerate(FARM_HAEUTE_H):
        skins = num(st["minuten"]) * rate / 60
        p["kf"][i] += skins
        for k in KEYS:
            p["f"][i][k] += skins * num(b[k])
        absorbed = min(skins, over_kills)
        st["absorbiert"].append(absorbed)
        for sec, kills, rb in over:
            share = absorbed * kills / over_kills
            for k in KEYS:
                per[sec]["adj"][i][k] -= share * num(rb[k])

cum_b = {"leder": START["leder"], "fetzen": START["fetzen"], "lhaut": 0.0, "mleder": 0.0, "mhaut": 0.0}
cum_o, cum_lo, cum_hi = dict(cum_b), dict(cum_b), dict(cum_b)
state, before_stop = {}, {}
for s in sections:
    p = per[s["abschnitt"]]
    before_stop[s["abschnitt"]] = {k: cum_lo[k] + p["b"][k] + p["adj"][0][k] for k in KEYS}   # Plan ohne den Farm-Stopp dieses Abschnitts
    for k in KEYS:
        cum_b[k] += p["b"][k]
        cum_o[k] += p["b"][k] + p["o"][k]
        cum_lo[k] += p["b"][k] + p["adj"][0][k] + p["f"][0][k]
        cum_hi[k] += p["b"][k] + p["adj"][1][k] + p["f"][1][k]
    state[s["abschnitt"]] = (dict(cum_b), dict(cum_o), dict(cum_lo), dict(cum_hi))

# --- Bedarf: Lederverarbeitung und Verzauberkunst bis ZIEL --------------------------------------------------------------
routes = {}
for r in need_rows:
    routes.setdefault((r["beruf"], r["route"]), []).append(r)


def crafts_of(r):
    """Herstellungen bis ZIEL; die letzte Stufe wird anteilig gezählt, wenn sie über ZIEL hinausgeht."""
    von, bis, n = num(r["von"]), num(r["bis"]), num(r["anzahl"])
    if von >= ZIEL:
        return 0.0
    if bis > ZIEL:
        return math.ceil(n * (ZIEL - von) / (bis - von))
    return n


def route_need(rs):
    cons, prod, crafts = {}, {}, {}
    for r in rs:
        key = (r["von"], r["rezept"])
        n = crafts_of(r)
        crafts[key] = n
        cons[r["material"]] = cons.get(r["material"], 0.0) + n * num(r["menge_je"])
    for (von, rezept), n in crafts.items():
        r = next(x for x in rs if x["von"] == von and x["rezept"] == rezept)
        if r["ergebnis"]:
            prod[r["ergebnis"]] = prod.get(r["ergebnis"], 0.0) + n * num(r["ergebnis_je"])
    net = {m: c - prod.get(m, 0.0) for m, c in cons.items() if c - prod.get(m, 0.0) > 1e-9}
    left = {m: p - cons.get(m, 0.0) for m, p in prod.items() if p - cons.get(m, 0.0) > 1e-9}
    return net, left, sum(crafts.values())


def de_yield(left):
    y, unknown = {}, []
    for item, n in left.items():
        d = de.get(item)
        if not d:
            if item not in ("Light Armor Kit", "Heavy Leather", "Cured Heavy Hide", "Cured Light Hide", "Cured Medium Hide", "Medium Leather", "Light Leather", "Forceful Heavy Armor Kit"):
                unknown.append(item)
            continue
        y[d["staub"]] = y.get(d["staub"], 0.0) + n * d["staub_je"]
        y[d["essenz"]] = y.get(d["essenz"], 0.0) + n * d["essenz_je"]
    return y, unknown


def lme_equiv(y):
    return y.get("Lesser Magic Essence", 0.0) + 3 * y.get("Greater Magic Essence", 0.0)   # 1 Greater = 3 Lesser (wow-professions; Messung 13.10.)


# Verzauberkunst: Staub-Weg als Basis, Essenzen ersetzen Staub stufenweise (bestes Verhältnis zuerst).
vz_staub = routes[("VZ", "wow-professions Staub")]
vz_essenz = routes[("VZ", "wow-professions Essenz")]
rng = {}
for r in vz_staub + vz_essenz:
    if r["material"] not in ("Strange Dust", "Lesser Magic Essence") or r["rezept"] == "Runed Silver Rod":
        continue
    k = (num(r["von"]), num(r["bis"]))
    side = "staub" if r["route"].endswith("Staub") else "essenz"
    rng.setdefault(k, {"staub": 0.0, "essenz": 0.0})[side] += crafts_of(r) * num(r["menge_je"])
ROD = {"staub": 3.0, "essenz": 4.0}                # Runed Silver Rod (beide Wege)
order = sorted(rng.items(), key=lambda kv: -(kv[1]["staub"] / kv[1]["essenz"]))   # Staub gespart pro Essenz


def vz_rest(sd, lme):
    """Was nach dem Einsatz von sd Staub und lme Essenzen für VZ 1-ZIEL noch fehlt (Staub, Essenz)."""
    need_sd = ROD["staub"] + sum(v["staub"] for _, v in rng.items())
    lme_left = lme - ROD["essenz"]
    miss_lme = max(0.0, -lme_left)
    lme_left = max(0.0, lme_left)
    for _, v in order:
        if lme_left <= 0:
            break
        part = min(1.0, lme_left / v["essenz"])
        need_sd -= part * v["staub"]
        lme_left -= part * v["essenz"]
    return max(0.0, need_sd - sd), miss_lme


def vz_plan(y):
    """Zusätzliche Embossed Leather Gloves (je 3 Leichtes Leder), bis der Ertrag für VZ 1-ZIEL reicht."""
    g = de[GLOVES]
    sd, lme = y.get("Strange Dust", 0.0), lme_equiv(y)
    rest0 = vz_rest(sd, lme)
    extra = 0
    while vz_rest(sd + extra * g["staub_je"], lme + extra * g["essenz_je"])[0] > 1e-9 and extra < 5000:
        extra += 1
    return rest0, extra


def variants(rs):
    """Zeilen einer Route je Variante (Spalte «variante», z. B. die zwei Tabs von wow-professions ab 130); leer gilt für alle."""
    vs = sorted({r.get("variante", "") for r in rs if r.get("variante")})
    if not vs:
        return [("", rs)]
    return [(v, [r for r in rs if r.get("variante", "") in ("", v)]) for v in vs]


lw = {}
for (beruf, name), rs in routes.items():
    if beruf != "LW":
        continue
    for v, vrs in variants(rs):
        net, left, n = route_need(vrs)
        y, unknown = de_yield(left)
        rest0, extra = vz_plan(y)
        lw[f"{name} ({v})" if v else name] = {"rows": vrs, "net": net, "left": left, "crafts": n, "de": y, "unknown": unknown,
                                              "vz_rest": rest0, "extra_gloves": extra}

vz_sd_total = ROD["staub"] + sum(v["staub"] for v in rng.values())
vz_lme_total = ROD["essenz"] + sum(v["essenz"] for v in rng.values())

# --- Bericht ----------------------------------------------------------------------------------------------------------
def main(OUT):
    LEDER_IDS.update({"Light Hide": "Light Hide", "Medium Hide": "Medium Hide"})   # deutsche Namen der Bälge im Testlog noch nicht gesehen
    L = ["# Mengenmodell Leder bis Stufe 20 (erzeugt von `tools/plan_mengen.py`)", "",
         f"Seit 14.10. gilt: Berufswechsel in Orgrimmar (Abschnitt {WECHSEL}, Stufe 16, Entscheidung des Nutzers). Danach gibt es kein eigenes Leder mehr; "
         f"die Zeilen nach {WECHSEL} zeigen nur, was die Route brächte, wenn Kürschnerei bliebe. Was mit dem Leder geschieht, steht in `docs/plan/berufe-plan.md` (`tools/plan_berufe.py`).", "",
         "Eingaben: `data/kombi/abschnitte.csv`, `modell_leder.csv`, `kuerschnern_anteile.csv`, `farmstellen.csv`, `farmstopps.csv`, `bedarf_lw_vz.csv`, "
         "dazu `data/rechnung/Kreislauf.csv` und `Preise.csv`. Nicht von Hand ändern, sondern die Eingaben anpassen und neu erzeugen.", "",
         "## Quellen", "",
         "- Route: RestedXP v4.11.23, `Guides/forever/Horde-1-12_Mulgore.lua` und `Horde-12-22_Barrens.lua` (https://github.com/RestedXP/RXPGuides), "
         "gelesen für Tauren-Druide mit RXPs Standard-Einstellungen in Forever (kein Hardcore, kein SSF, keine Dungeons, XP-Rate 1). Schrittnummern so, wie RXP sie diesem Charakter zeigt.",
         "- Anzahlen: RXPs Kommentare an den `.complete`-Zeilen. Stufe am Ende jedes Abschnitts: RXPs `.xp`-Schritte (Spalte «Beleg Stufe»).",
         "- Gegnerstufen: Warcraft Tavern, Hunter-Pets-Seiten (Classic) · MetaForge, Seite «Medium Hide» (VMaNGOS-Daten) · Best Practice §9.",
         "- Anteile beim Kürschnern: Testlog 13.10. (Mulgore) · MetaForge Zhevra Runner und Zhevra Charger (Best Practice §9).",
         "- Wowhead, «Classic Leather Farming: Early Leather» (RenataKane, Stand 09.06.2021): Leichtes Leder am besten von Gegnern der Stufe 11–20, "
         "Mittleres Leder ab 16 (am besten 21–30), Bälge 3–5 %, ab Stufe 11 bis zu 2 Leichtes Leder pro Haut (Classic). https://cn.classic.wowhead.com/guides/classic-leather-farming-early-leather",
         "- Lederverarbeitung 1–150: wow-professions, Leatherworking Leveling Guide (Forever-Beta) https://www.wow-professions.com/forever/leatherworking-leveling-guide · "
         "kami-labs, Leatherworking Guide (Stand 08.10.) https://kami-labs.fr/en/guide-travail-du-cuir-wow-forever/",
         "- Verzauberkunst 1–150: wow-professions, Enchanting Leveling Guide (Forever-Beta) https://www.wow-professions.com/forever/enchanting-leveling-guide",
         "- Entzaubern und Preise: `data/rechnung/Kreislauf.csv` (wow-professions-Tabelle), `Preise.csv` (AHledger, Beta, Horde US).", "",
         "## Annahmen", "",
         f"- Bestand am Start: {START['leder']} Leichtes Leder, {START['fetzen']} Verdorbene Lederfetzen (Testlog 13.10. 22:42).",
         f"- Kills je Quest-Gegenstand: 2 (Annahme), je Kill-Ziel oder benanntem Gegner: 1. Gemessen: {KILLS_JE_STUECK_GEMESSEN}.",
         "- Jede Haut gibt 1 Gegenstand (Testlog 13.10., 21 von 21 Häuten, Gegner Stufe 5–8). Dass ab Gegnerstufe 11 bis zu 2 Leder kommen (Wowhead, Classic), ist nicht eingerechnet.",
         "- Quest 768 «Gathering Leather» nimmt 12 Leichtes Leder (Abschnitt B2). Wer sie überspringt, hat 12 mehr.",
         "- «Basis» = Quest-Tiere, die die Route sicher tötet. «Option» = Kürschnerbarkeit ungeprüft oder optionale Grind-Schritte. "
         "Tiere, die nebenbei sterben, zählt das Modell nicht; das Testlog misst sie (SAMMELN mit Kreatur-ID).",
         f"- Farm-Stopps: Minuten aus `farmstopps.csv` (Vorschlag zum Testen), {FARM_HAEUTE_H[0]}–{FARM_HAEUTE_H[1]} Häute pro Stunde (Annahme, keine Quelle für Stufe 12–20). "
         "Zum Vergleich gemessen: rund 97 Häute pro Stunde in Mulgore, Charakter Stufe 6–7 gegen Gegner der Stufe 5–8, neben Quest 748 (Testlog 13.10., 21 Häute in rund 13 Minuten). "
         "«Plan» = Basis plus Farm-Stopps mit der unteren Rate. Kills an Tieren, die eine Quest der Route ohnehin braucht, zählen beim Farm-Stopp nicht doppelt (Spalte «ueberschneidet» in `farmstopps.csv`).",
         f"- Kürschnerei endet mit dem Wechsel in Orgrimmar (Ende {WECHSEL}). Die früheren Farm-Stopps S2 (Südbrachland) und S3 (Camp Taurajo) lagen danach und entfallen.",
         "- Kein Farm-Stopp gleich bei der Ankunft in den Crossroads: Die Route tötet dort sofort dieselben Tiere für «Plainstrider Menace» (844, 7 Schnäbel), «Raptor Thieves» (869, 12 Köpfe) und «The Zhevra» (845, 4 Hufe), zusammen rund 46 Kills. Ein Stopp davor würde diese Kills nur vorziehen und kein zusätzliches Leder bringen.", "",
         "## Anteile beim Kürschnern nach Gegnerstufe", "",
         "| Band | Gegnerstufe | Leichtes Leder | Fetzen | Light Hide | Mittleres Leder | Medium Hide | Quelle |", "|---|---|---|---|---|---|---|---|"]
    for b in bands:
        L.append(f"| {b['band']} | {b['stufe_von']}–{b['stufe_bis']} | {num(b['leder']):.0%} | {num(b['fetzen']):.0%} | {num(b['lhaut']):.0%} | {num(b['mleder']):.0%} | {num(b['mhaut']):.0%} | {b['quelle']} |")

    stop_by_sec = {}
    for st in stops:
        stop_by_sec.setdefault(st["abschnitt"], []).append(st)
    L += ["", "## Route: Abschnitte und Bestand", "",
          "Leichtes Leder kumuliert: Basis · Plan mit Farm-Stopps (untere bis obere Rate) · mit Optionen statt Farm-Stopps.", "",
          "| Abschnitt | RXP-Schritte | bis | Stufe am Ende | Kills Basis (Option) | Farm-Stopp | Leichtes Leder Basis | Plan | mit Optionen | Mittleres Leder Basis / Plan | Fetzen (Plan) | Light Hide (Plan) | Beleg Stufe |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for s in sections:
        p = per[s["abschnitt"]]
        cb, co, clo, chi = state[s["abschnitt"]]
        sts = stop_by_sec.get(s["abschnitt"], [])
        fs = "; ".join(f"{x['id']} {x['minuten']} min, {num(x['minuten']) * FARM_HAEUTE_H[0] / 60:.0f}–{num(x['minuten']) * FARM_HAEUTE_H[1] / 60:.0f} Häute"
                       + (f", davon bis {max(x['absorbiert']):.0f} für Quest {x['ueberschneidet']}" if x.get("ueberschneidet") else "") for x in sts) or "–"
        L.append(f"| {s['abschnitt']} | {s['guide']} {s['schritte']} | {s['bis']} | {s['stufe_ende']} | {p['kb']:.0f} ({p['ko']:.0f}) | {fs} | "
                 f"{cb['leder']:.0f} | {clo['leder']:.0f}–{chi['leder']:.0f} | {co['leder']:.0f} | {cb['mleder']:.0f} / {clo['mleder']:.0f} | {clo['fetzen']:.0f} | {clo['lhaut']:.1f} | {s['stufe_beleg']} |")

    s15, o15, p15, h15 = state[STAND_15]
    s20, o20, p20, h20 = state[STAND_20]
    sw, ow, pw, hw = state[WECHSEL]
    L += ["", f"**Stand beim Wechsel in Orgrimmar** (Ende Abschnitt {WECHSEL}, Stufe 16): Basis {sw['leder']:.0f} Leichtes Leder, Plan {pw['leder']:.0f}–{hw['leder']:.0f}, "
          f"dazu {pw['fetzen']:.0f}–{hw['fetzen']:.0f} Fetzen, {pw['lhaut']:.1f}–{hw['lhaut']:.1f} Light Hide. Daraus rechnet `tools/plan_berufe.py` den Sweetspot.",
          f"**Stand bei Stufe 15** (Ende Abschnitt {STAND_15}): Basis {s15['leder']:.0f} Leichtes Leder, Plan {p15['leder']:.0f}–{h15['leder']:.0f}, "
          f"dazu {p15['fetzen']:.0f} Fetzen, {p15['lhaut']:.1f} Light Hide.",
          f"**Stand bei Stufe 20, nur falls Kürschnerei bliebe** (Ende Abschnitt {STAND_20}): Basis {s20['leder']:.0f} Leichtes Leder, Plan {p20['leder']:.0f}–{h20['leder']:.0f}, "
          f"dazu {p20['mleder']:.0f} Mittleres Leder (Basis {s20['mleder']:.0f}), {p20['fetzen']:.0f} Fetzen, {p20['lhaut']:.1f} Light Hide, {p20['mhaut']:.1f} Medium Hide.", "",
          "## Ziele im Kombi-Guide", "",
          f"Zähler (Bank zählt mit) = Plan vor dem Farm-Stopp des Abschnitts; Farm-Stopp = Plan danach. Abgerundet. Nur bis zum Wechsel ({WECHSEL}).", "",
          "| Abschnitt | Zähler bis Abschnittsende | Mittleres Leder bis dahin | Farm-Stopp | Ziel Farm-Stopp | Mittleres Leder nach dem Farm-Stopp |", "|---|---|---|---|---|---|"]
    for s in sections[:sec_ids.index(WECHSEL) + 1]:
        sid = s["abschnitt"]
        bf = before_stop[sid]
        after = state[sid][2]
        st = stop_by_sec.get(sid)
        stop_txt = ", ".join(f"{x['id']} {spot_by[x['farmstelle']]['name']} ({x['minuten']} min)" for x in st) if st else "–"
        goal = f"{math.floor(after['leder'])}" if st else "–"
        L.append(f"| {sid} | {math.floor(bf['leder'])} | {math.floor(bf['mleder'])} | {stop_txt} | {goal} | {math.floor(after['mleder']) if st else '–'} |")
    L += ["", "Seit v0.4 zeigt der Zähler beim Farm-Stopp S1 nicht den Modellwert, sondern den Sweetspot für Lederverarbeitung 1–80 "
          "(62 Leichtes Leder, `docs/plan/berufe-plan.md`)."]

    L += ["", f"## Bedarf für Lederverarbeitung {ZIEL} und Verzauberkunst {ZIEL}", "",
          f"Die zwei Forever-Routen für Lederverarbeitung widersprechen sich stark. Die letzte Stufe einer Route wird bis {ZIEL} anteilig gezählt. "
          "Netto heisst: was die Route selbst herstellt (z. B. Leichtes Leder aus Fetzen, Mittleres Leder aus Leichtem Leder), ist abgezogen.", "",
          "| Material | " + " | ".join(f"LW {n}" for n in lw) + " | AH-Rechenpreis |", "|---|" + "---|" * len(lw) + "---|"]
    mats = []
    for v in lw.values():
        for m in v["net"]:
            if m not in mats:
                mats.append(m)
    first = ["Light Leather", "Ruined Leather Scraps", "Medium Leather", "Light Hide", "Medium Hide", "Heavy Hide"]
    mats = [m for m in first if m in mats] + [m for m in mats if m not in first]
    for m in mats:
        name = LEDER_IDS.get(m, m)
        L.append(f"| {name} | " + " | ".join(f"{v['net'].get(m, 0):.0f}" for v in lw.values()) + f" | {silber(prices[m]) if m in prices else 'kein Preis'} |")
    L += ["", "Was die Herstellung für Verzauberkunst liefert (Erwartungswert, Entzaubern der übrigen grünen Teile nach `Kreislauf.csv`):", ""]
    for n, v in lw.items():
        left = ", ".join(f"{c:.0f} {i}" for i, c in v["left"].items())
        yld = ", ".join(f"{c:.1f} {i}" for i, c in v["de"].items() if c > 0)
        unk = f" Ohne Entzauberungswert in `Kreislauf.csv`: {', '.join(v['unknown'])}." if v["unknown"] else ""
        L.append(f"- LW {n}: übrig {left}. Entzaubern ergibt etwa {yld}.{unk}")
    L += ["", f"Verzauberkunst 1–{ZIEL} (wow-professions): Staub-Weg {vz_sd_total:.0f} Strange Dust und {ROD['essenz']:.0f} Lesser Magic Essence, "
          f"Essenz-Weg {vz_lme_total:.0f} Lesser Magic Essence und {ROD['staub']:.0f} Strange Dust, dazu Copper Rod, 19 Mote of Magic, Silver Rod, Shadowgem. "
          "Das Modell nimmt den Staub-Weg und setzt eigene Essenzen dort ein, wo eine Essenz am meisten Staub spart (1 Greater = 3 Lesser).", "",
          "| | " + " | ".join(f"mit LW {n}" for n in lw) + " |", "|---|" + "---|" * len(lw),
          "| Strange Dust, der nach dem eigenen Entzaubern fehlt | " + " | ".join(f"{v['vz_rest'][0]:.0f}" for v in lw.values()) + " |",
          f"| dafür zusätzliche {GLOVES} (je 3 Leichtes Leder) | " + " | ".join(f"{v['extra_gloves']}" for v in lw.values()) + " |",
          "| = zusätzliches Leichtes Leder für Verzauberkunst | " + " | ".join(f"{3 * v['extra_gloves']}" for v in lw.values()) + " |",
          "| oder Strange Dust im AH kaufen (Beta) | " + " | ".join(f"{silber(v['vz_rest'][0] * prices['Strange Dust'])}" for v in lw.values()) + " |", ""]

    L += ["## Lücke: Leichtes Leder", "",
          "Bedarf = Lederverarbeitung netto, ohne oder mit dem Leder für Verzauberkunst. Angebot = Plan (Basis plus Farm-Stopps, untere Rate). "
          f"Farmzeit für den Rest bei {FARM_HAEUTE_H[0]}–{FARM_HAEUTE_H[1]} Häuten pro Stunde und dem Leder-Anteil der Stufe 11–15 bzw. 16–20.", "",
          "| Sammeln bis | LW-Route | Bedarf | Angebot (Plan) | Lücke | weitere Farmzeit | oder AH (Beta) |", "|---|---|---|---|---|---|---|"]
    b2, b3 = band_of(13), band_of(18)
    gaps = {}
    for label, st, bb in ((f"Wechsel ({WECHSEL}, Stufe 16)", pw, b2), ("Stufe 20, falls Kürschnerei bliebe", p20, b3)):
        lo, hi = FARM_HAEUTE_H[0] * num(bb["leder"]), FARM_HAEUTE_H[1] * num(bb["leder"])
        for n, v in lw.items():
            for with_vz in (False, True):
                need = v["net"].get("Light Leather", 0.0) + (3 * v["extra_gloves"] if with_vz else 0)
                gap = max(0.0, need - st["leder"])
                gaps[(label, n, with_vz)] = (need, gap, gap / hi, gap / lo)
                what = f"{n}" + (" + VZ aus eigenem Entzaubern" if with_vz else "")
                L.append(f"| {label} | {what} | {need:.0f} | {st['leder']:.0f} | {gap:.0f} | {gap / hi:.1f}–{gap / lo:.1f} h | {silber(gap * prices['Light Leather'])} |")
    L += ["", "Mittleres Leder, Bälge und Fetzen (Plan bis zum Wechsel gegen Bedarf):", "",
          "| Material | Plan bis zum Wechsel | " + " | ".join(f"Bedarf LW {n}" for n in lw) + " |", "|---|---|" + "---|" * len(lw)]
    for m, key in (("Medium Leather", "mleder"), ("Ruined Leather Scraps", "fetzen"), ("Light Hide", "lhaut"), ("Medium Hide", "mhaut")):
        L.append(f"| {LEDER_IDS[m]} | {pw[key]:.0f} | " + " | ".join(f"{v['net'].get(m, 0):.0f} (Lücke {max(0, v['net'].get(m, 0) - pw[key]):.0f}, AH {silber(max(0, v['net'].get(m, 0) - pw[key]) * prices[m])})" for v in lw.values()) + " |")

    L += ["", "## Farmstellen entlang der Route (Mitte der RXP-Schleifen, Brachland-Karte 1413 mit exakten Ecken)", "",
          "| Id | Ort | x, y | Tiere | Stufe | RXP-Bezug | Hinweis |", "|---|---|---|---|---|---|---|"]
    for f in spots:
        L.append(f"| {f['id']} | {f['name']} | {f['x']}, {f['y']} | {f['tiere']} | {f['stufen']} | {f['rxp_bezug']} | {f['hinweis']} |")
    L += ["", "Farm-Stopps im Kombi-Guide (`farmstopps.csv`):", "", "| Id | Abschnitt | Farmstelle | Minuten | überschneidet Quest | Wo im Guide | Quelle |", "|---|---|---|---|---|---|---|"]
    for st in stops:
        L.append(f"| {st['id']} | {st['abschnitt']} | {st['farmstelle']} {spot_by[st['farmstelle']]['name']} | {st['minuten']} | {st.get('ueberschneidet') or '–'} | {st['wo_im_guide']} | {st['quelle']} |")

    L += ["", "## Zeilen", "", "| Abschnitt | RXP-Schritte | Quest | Ziel | Kreatur | Stufe | Band | Kills | Art | Quelle |", "|---|---|---|---|---|---|---|---|---|---|"]
    for r, kills, band in detail:
        L.append(f"| {r['abschnitt']} | {r['rxp_schritte']} | {r['quest']} | {r['ziel']} | {r['kreatur']} | {r['kreatur_stufe']} | {band} | {kills:.0f} | {r['art']} | {r['quelle']} |")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")
    for s in sections:
        sid = s["abschnitt"]
        print(f"{sid} (Stufe {s['stufe_ende']}): Basis {state[sid][0]['leder']:.1f} | Zähler vor Farm-Stopp {before_stop[sid]['leder']:.1f} (ML {before_stop[sid]['mleder']:.1f}) | Plan {state[sid][2]['leder']:.1f}–{state[sid][3]['leder']:.1f} | ML Plan {state[sid][2]['mleder']:.1f}")
    for n, v in lw.items():
        print(f"LW {n}: netto " + ", ".join(f"{c:.0f} {m}" for m, c in v["net"].items()) + f" | VZ: fehlen {v['vz_rest'][0]:.0f} Staub -> {v['extra_gloves']} Handschuhe")
    for k, (need, gap, h1, h2) in gaps.items():
        print(f"Lücke {k}: Bedarf {need:.0f}, Lücke {gap:.0f}, {h1:.1f}-{h2:.1f} h")
    print(f"Bericht: {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "docs", "plan", "mengen-leder.md"))
