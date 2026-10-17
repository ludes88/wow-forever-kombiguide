# Kampfdaten aus dem Testlog (ab Testlog 4.0): Schaden, Heilung, erlittene Treffer, Rotation, Werte, Ausrüstung, Talente,
# Quest-Belohnungen, dazu Fischglas gegen Lagerstuhl mit den gemessenen Werten.
#
# Aufruf:  python3 tools/kampf_aus_testlog.py <KombiTestlog.lua> [weitere Testlog-Dateien …]
#          python3 tools/kampf_aus_testlog.py --gewichte [StatWeights.lua]   RXP-Gewichte neu übernehmen
#                                             (ohne Pfad: vendor/rxpguides/DB/forever/StatWeights.lua, tools/fetch_rxp.sh)
#
# Liest aus der SavedVariables-Datei (Testlog 4.0): chars[Charakter].kampf (pro Kampf), .werte (letzter Stand pro Gestalt),
# .werteLog, .ausruestung, .talente, .belohnungen, .klasse, dazu itemWerte, itemTexte, info und zauberNamen.
# Schreibt ins Repo nur Zahlen ohne Charakter- und Realmnamen und ohne Uhrzeiten (nur das Datum):
#   data/spiel/kampf.csv          eine Zeile pro Kampf; Kennung = Prüfwert (SHA-256, 8 Zeichen) aus Charakter und Startzeit
#   data/spiel/kampf_zauber.csv   pro Kampf und Zauber: Anzahl Zauber, Schaden, Heilung, erlittener Schaden (Schadensmesser)
#   data/spiel/werte.csv          pro Klasse, Stufe und Gestalt der neueste Stand der Werte mit der Umrechnung des Clients
#   docs/plan/kampf.md            Bericht
# Neue Zeilen kommen dazu, gleiche Schlüssel werden ersetzt; so wächst der Verlauf über mehrere Testlogs.
# Gewichte: data/kampf/gewichte_rxp.csv aus RestedXP v4.11.23, DB/forever/StatWeights.lua (CC BY-NC-SA 4.0,
#   https://github.com/RestedXP/RXPGuides). «Krit», «Treffer», «Ausweichen» und «Parieren» gelten dort pro 1 %: RXP liest
#   «Improves your chance to get a critical strike by N%» usw. aus dem Tooltip (ItemUpgrades.lua, OUT_OF_BAND_KEYS; nur
#   englische und französische Texte). Gewichte sind RXPs Zahlen für das Leveln, kein Messwert.
# Fischglas +8 % Werte, Lagerstuhl +2 % Krit mit allen Zaubern und Angriffen (Tooltips laut MetaForge, Forever, Build 70170,
#   abgerufen 17.10.2026). Welche Werte das Glas erhöht, sagt der Tooltip nicht genau; gerechnet wird mit den fünf Grundwerten.
import csv, hashlib, os, re, statistics, sys
from collections import Counter, defaultdict
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ah_aus_testlog as at  # noqa: E402  (Lua-Datei lesen, CSV schreiben)

ROOT = at.ROOT
D = os.path.join(ROOT, "data", "spiel")
GEWICHTE = os.path.join(ROOT, "data", "kampf", "gewichte_rxp.csv")
RXP_WEIGHTS = os.path.join(ROOT, "vendor", "rxpguides", "DB", "forever", "StatWeights.lua")
BERICHT = os.path.join(ROOT, "docs", "plan", "kampf.md")
USAGE = "Aufruf: python3 tools/kampf_aus_testlog.py <KombiTestlog.lua> [weitere …] | --gewichte [StatWeights.lua]"
QUELLE_RXP = "RestedXP v4.11.23 DB/forever/StatWeights.lua (CC BY-NC-SA 4.0, https://github.com/RestedXP/RXPGuides)"
GLAS, STUHL = 0.08, 2.0
MANA_JE_INT = 15   # Warcraft Tavern (Forever): «Intellect gives 15 mana», https://www.warcrafttavern.com/forever/guides/stats/
WERTE = ["str", "agi", "sta", "int", "spi"]
WERTE_DE = {"str": "Stärke", "agi": "Beweglichkeit", "sta": "Ausdauer", "int": "Intellekt", "spi": "Willenskraft"}
STAT_KEY = {"str": "ITEM_MOD_STRENGTH_SHORT", "agi": "ITEM_MOD_AGILITY_SHORT", "sta": "ITEM_MOD_STAMINA_SHORT",
            "int": "ITEM_MOD_INTELLECT_SHORT", "spi": "ITEM_MOD_SPIRIT_SHORT"}
KURZ = {"ITEM_MOD_STRENGTH_SHORT": "Stä", "ITEM_MOD_AGILITY_SHORT": "Bew", "ITEM_MOD_STAMINA_SHORT": "Aus",
        "ITEM_MOD_INTELLECT_SHORT": "Int", "ITEM_MOD_SPIRIT_SHORT": "Wil", "RESISTANCE0_NAME": "Rüstung",
        "ITEM_MOD_DAMAGE_PER_SECOND_SHORT": "DPS", "ITEM_MOD_ATTACK_POWER_SHORT": "AP",
        "ITEM_MOD_CRIT_RATING_SHORT": "Krit %", "ITEM_MOD_HIT_RATING_SHORT": "Treffer %",
        "ITEM_MOD_DODGE_RATING_SHORT": "Ausweichen %", "ITEM_MOD_PARRY_RATING_SHORT": "Parieren %"}
# Tooltip-Zeilen (Testlog itemTexte, deutscher Client) -> RXP-Schlüssel; die Muster sind eine Annahme (Wortlaut in Forever
# ungeprüft), Treffer stehen im Bericht mit «aus dem Tooltip»
TEXT_MUSTER = [(r"kritisch\w*[^%]*?(\d+)\s*%", "ITEM_MOD_CRIT_RATING_SHORT"),
               (r"ausweich\w*[^%]*?(\d+)\s*%", "ITEM_MOD_DODGE_RATING_SHORT"),
               (r"parier\w*[^%]*?(\d+)\s*%", "ITEM_MOD_PARRY_RATING_SHORT"),
               (r"treff\w*[^%]*?(\d+)\s*%", "ITEM_MOD_HIT_RATING_SHORT")]
KLASSE_RXP = {"DRUID": "Druid", "WARRIOR": "Warrior", "PALADIN": "Paladin", "HUNTER": "Hunter", "ROGUE": "Rogue",
              "PRIEST": "Priest", "SHAMAN": "Shaman", "MAGE": "Mage", "WARLOCK": "Warlock"}
KLASSE_DE = {"DRUID": "Druide", "WARRIOR": "Krieger", "PALADIN": "Paladin", "HUNTER": "Jäger", "ROGUE": "Schurke",
             "PRIEST": "Priester", "SHAMAN": "Schamane", "MAGE": "Magier", "WARLOCK": "Hexenmeister"}
SLOTS = ["Kopf", "Hals", "Schulter", "Hemd", "Brust", "Taille", "Beine", "Füsse", "Handgelenke", "Hände", "Finger 1",
         "Finger 2", "Schmuck 1", "Schmuck 2", "Rücken", "Waffenhand", "Schildhand", "Distanz", "Wappenrock"]
AUSW_DE = {"DODGE": "ausgewichen", "PARRY": "pariert", "MISS": "verfehlt", "BLOCK": "geblockt", "RESIST": "widerstanden",
           "ABSORB": "absorbiert", "IMMUNE": "immun", "EVADE": "entkommen", "DEFLECT": "abgelenkt", "REFLECT": "reflektiert"}
F = {
    "kampf": ["kennung", "datum", "klasse", "stufe", "gestalt", "gestalten", "dauer_s", "gegner", "gruppe", "schaden",
              "schaden_pro_s", "heilung", "erlitten_messer", "erlitten", "erlitten_treffer", "erlitten_krit",
              "erlitten_schmetternd", "vermieden", "geheilt", "am_ziel", "am_ziel_treffer", "am_ziel_krit",
              "am_ziel_vermieden", "zauber", "folge", "schlaege", "schlag_s", "xp", "tod", "leben_start", "leben_ende", "mana_start",
              "mana_ende", "quelle_schaden", "geheim", "testlog"],
    "kampf_zauber": ["kennung", "zauber", "name", "anzahl", "schaden", "heilung", "erlitten"],
    "werte": ["klasse", "stufe", "gestalt", "datum", "str", "agi", "sta", "int", "spi", "ap", "waffe", "tempo", "krit",
              "zauberkrit", "ausweichen", "parieren", "ruestung", "leben", "mana", "zaubermacht", "heilung", "treffer",
              "regen", "verteidigung", "umrechnung", "anlass", "testlog"],
}


def kennung(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:8]


def zahl(v):
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    return int(f) if f.is_integer() else f


def kv(s):
    """«a:b;c:d» -> {a: b}; Werte als Zahl, wo möglich."""
    out = {}
    for teil in str(s or "").split(";"):
        if ":" in teil:
            k, v = teil.split(":", 1)
            z = zahl(v)
            out[zahl(k) if zahl(k) is not None else k] = z if z is not None else v
    return out


def leer(s):
    return "" if s in (None, "") else str(s).replace(";", " ")


# --- RXP-Gewichte ---------------------------------------------------------------------------------------------------------
def gewichte_aus_rxp(pfad):
    src = open(pfad, encoding="utf-8").read()
    rows = []
    for m in re.finditer(r"\['([^']+)'\] = \{(.*?)\n    \},", src, re.S):
        d = {"profil": m.group(1), "quelle": QUELLE_RXP}
        for k, v in re.findall(r"\['([A-Za-z_0-9]+)'\] = \"?([^\",\n]+)\"?,", m.group(2)):
            d[k] = v.strip()
        rows.append(d)
    return rows


def gewichte_schreiben(pfad):
    rows = gewichte_aus_rxp(pfad)
    stats = sorted({k for r in rows for k in r if k.isupper() and k not in ("MIN_LEVEL", "MAX_LEVEL")})
    felder = ["profil", "Class", "Spec", "Kind", "MIN_LEVEL", "MAX_LEVEL"] + stats + ["quelle"]
    at._write(GEWICHTE, felder, rows)
    return len(rows)


def gewichte():
    if not os.path.exists(GEWICHTE):
        return []
    out = []
    for r in at._read(GEWICHTE):
        e = {k: (zahl(v) if zahl(v) is not None else v) for k, v in r.items()}
        out.append(e)
    return out


def profil(gew, klasse, stufe, spec, art="Speedrun"):
    name = KLASSE_RXP.get(klasse)
    for r in gew:
        if (r.get("Class") == name and r.get("Spec") == spec and r.get("Kind") == art
                and int(r.get("MIN_LEVEL") or 0) <= (stufe or 0) <= int(r.get("MAX_LEVEL") or 0)):
            return r
    return None


def specs(gew, klasse):
    name = KLASSE_RXP.get(klasse)
    return sorted({r.get("Spec") for r in gew if r.get("Class") == name and r.get("Spec")})


def punkte(stats, w):
    """Gewichtete Summe eines Gegenstands (RXP-Schlüssel -> Wert) mit einem Profil."""
    if not w:
        return None
    return sum(float(w.get(k) or 0) * float(v) for k, v in stats.items() if isinstance(v, (int, float)))


# --- Lesen -------------------------------------------------------------------------------------------------------------------
def lade(pfade):
    daten = {"kampf": {}, "werte": {}, "chars": {}, "itemWerte": {}, "itemTexte": {}, "info": {}, "zauber": {}}
    for p in pfade:
        db = at._py(at._lua_tabelle(open(p, encoding="utf-8", errors="replace").read()))
        for k, v in (db.get("itemWerte") or {}).items():
            daten["itemWerte"][str(k)] = str(v or "")
        for k, v in (db.get("itemTexte") or {}).items():
            daten["itemTexte"][str(k)] = str(v or "")
        info = db.get("info") or {}
        for k, v in (info.items() if isinstance(info, dict) else enumerate(info, 1)):
            if isinstance(v, dict):
                daten["info"][int(k)] = v
        zn = db.get("zauberNamen") or {}
        for k, v in (zn.items() if isinstance(zn, dict) else enumerate(zn, 1)):
            daten["zauber"][int(k)] = str(v)
        for key, c in (db.get("chars") or {}).items():
            if not isinstance(c, dict):
                continue
            ch = kennung(str(key))
            klasse = str(c.get("klasse") or "?")
            for r in (c.get("kampf") or []):
                if isinstance(r, dict) and r.get("t") is not None:
                    daten["kampf"][kennung(f"{key}|{r.get('t')}")] = (klasse, r)
            for w in (c.get("werteLog") or []):
                if isinstance(w, dict) and w.get("t") is not None:
                    alt = daten["werte"].get((klasse, zahl(w.get("lvl")), w.get("form")))
                    if not alt or (alt.get("t") or 0) <= (w.get("t") or 0):
                        daten["werte"][(klasse, zahl(w.get("lvl")), w.get("form"))] = w
            e = daten["chars"].setdefault(ch, {"klasse": klasse})
            neu = max([zahl(w.get("t")) or 0 for w in (c.get("werteLog") or []) if isinstance(w, dict)] + [0])
            if neu >= e.get("t", -1):
                aus = c.get("ausruestung") or {}
                e.update({"t": neu, "ausruestung": dict(enumerate(aus, 1)) if isinstance(aus, list) else aus,
                          "talente": c.get("talente"), "werte": c.get("werte") or {},
                          "stufe": max([zahl(w.get("lvl")) or 0 for w in (c.get("werteLog") or []) if isinstance(w, dict)] + [0])})
            bel = e.setdefault("belohnungen", {})
            for b in (c.get("belohnungen") or []):
                if isinstance(b, dict):
                    bel[f"{b.get('t')}|{b.get('q')}|{b.get('items')}|{b.get('wahl')}"] = b
    return daten


def item_stats(daten, schluessel=None, item_id=None):
    """Werte eines Gegenstands (RXP-Schlüssel -> Zahl) aus itemWerte, dazu Prozent-Effekte aus den Tooltip-Zeilen."""
    s, txt = None, None
    if schluessel is not None:
        s, txt = daten["itemWerte"].get(schluessel), daten["itemTexte"].get(schluessel)
    if s is None and item_id is not None:
        for k, v in daten["itemWerte"].items():
            if re.match(r"item:%d(:|$)" % int(item_id), k):
                s, txt = v, daten["itemTexte"].get(k)
                break
    out, aus_text = {}, []
    for teil in (s or "").split(";"):
        if "=" in teil:
            k, v = teil.split("=", 1)
            if zahl(v) is not None:
                out[k] = zahl(v)
    for zeile in (txt or "").split(" / "):
        for muster, key in TEXT_MUSTER:
            m = re.search(muster, zeile, re.I)
            if m:
                out[key] = out.get(key, 0) + int(m.group(1))
                aus_text.append(key)
                break
    return out, aus_text, txt


def stats_text(stats, aus_text):
    teile = []
    for k, v in sorted(stats.items()):
        name = KURZ.get(k, k.replace("ITEM_MOD_", "").replace("_SHORT", ""))
        teile.append(f"{name} {v}" + (" (aus dem Tooltip)" if k in aus_text else ""))
    return ", ".join(teile) or "keine Werte"


# --- Zeilen ------------------------------------------------------------------------------------------------------------------
def _dm(r, art):
    dm = r.get("dm") if isinstance(r.get("dm"), dict) else {}
    e = dm.get(art) if isinstance(dm.get(art), dict) else None
    return e


def kampf_zeilen(daten):
    out = []
    for k, (klasse, r) in sorted(daten["kampf"].items(), key=lambda kv_: kv_[1][1].get("t") or 0):
        d = float(r.get("d") or 0)
        sch, hei, erl = _dm(r, "schaden"), _dm(r, "heilung"), _dm(r, "erlitten")
        inn = (str(r.get("inn") or "0:0").split(":") + ["0", "0"])[:2]
        innf = kv(r.get("innF"))
        ziel = (str(r.get("amZiel")).split(":") + ["", ""])[:2] if r.get("amZiel") else ["", ""]
        zf, za = kv(r.get("amZielF")), kv(r.get("amZielA"))
        lp0 = (str(r.get("lp0") or "").split(":") + [""] * 6)[:6]
        lp1 = (str(r.get("lp1") or "").split(":") + [""] * 6)[:6]
        casts = kv(r.get("casts"))
        out.append({
            "kennung": k, "datum": datetime.fromtimestamp(int(float(r.get("t") or 0))).strftime("%Y-%m-%d"),
            "klasse": klasse, "stufe": zahl(r.get("lvl")), "gestalt": r.get("form"), "gestalten": r.get("formen"),
            "dauer_s": f"{d:.1f}", "gegner": leer(r.get("ziel")), "gruppe": r.get("gruppe") or "",
            "schaden": sch["sum"] if sch else "", "schaden_pro_s": f"{sch['sum'] / d:.1f}" if sch and d > 0 else "",
            "heilung": hei["sum"] if hei else "", "erlitten_messer": erl["sum"] if erl else "",
            "erlitten": inn[1], "erlitten_treffer": inn[0], "erlitten_krit": innf.get("CRITICAL", 0),
            "erlitten_schmetternd": innf.get("CRUSHING", 0), "vermieden": leer(r.get("ausw")),
            "geheilt": (str(r.get("heilIn") or "0:0").split(":") + ["0"])[1], "am_ziel": ziel[1], "am_ziel_treffer": ziel[0],
            "am_ziel_krit": zf.get("CRITICAL", "") if r.get("amZiel") else "",
            "am_ziel_vermieden": sum(v for v in za.values() if isinstance(v, int)) if r.get("amZiel") else "",
            "zauber": sum(v for v in casts.values() if isinstance(v, int)), "folge": str(r.get("folge") or "").replace(";", " "),
            "schlaege": zahl(r.get("swing")) or 0, "schlag_s": r.get("swingDauer") or "", "xp": zahl(r.get("xp")) or 0,
            "tod": r.get("tod") or "",
            "leben_start": lp0[0], "leben_ende": lp1[0], "mana_start": lp0[4], "mana_ende": lp1[4],
            "quelle_schaden": "Schadensmesser" if sch else (r.get("dmGrund") or ""),
            "geheim": leer(" ".join(x for x in (r.get("geheim"), r.get("einschr")) if x)), "testlog": r.get("v")})
    return out


def zauber_zeilen(daten):
    out = []
    for k, (klasse, r) in daten["kampf"].items():
        z = defaultdict(dict)
        for sid, n in kv(r.get("casts")).items():
            z[sid]["anzahl"] = n
        for art, feld in (("schaden", "schaden"), ("heilung", "heilung"), ("erlitten", "erlitten")):
            e = _dm(r, art)
            for sid, v in kv(e.get("z") if e else "").items():
                z[sid][feld] = v
        for sid, e in z.items():
            out.append({"kennung": k, "zauber": sid, "name": daten["zauber"].get(sid, ""), "anzahl": e.get("anzahl", 0),
                        "schaden": e.get("schaden", ""), "heilung": e.get("heilung", ""), "erlitten": e.get("erlitten", "")})
    return out


def eff(w, k):
    teile = str(w.get(k) or "").split(":")
    return zahl(teile[1]) if len(teile) > 1 else None


def werte_zeilen(daten):
    out = []
    for (klasse, lvl, form), w in sorted(daten["werte"].items(), key=lambda x: (x[0][0], x[0][1] or 0, str(x[0][2]))):
        ap = sum(zahl(x) or 0 for x in str(w.get("ap") or "").split(":")) if w.get("ap") else ""
        out.append({"klasse": klasse, "stufe": lvl, "gestalt": form,
                    "datum": datetime.fromtimestamp(int(float(w.get("t") or 0))).strftime("%Y-%m-%d"),
                    **{k: eff(w, k) for k in WERTE}, "ap": ap, "waffe": w.get("dmg"), "tempo": w.get("tempo"),
                    "krit": w.get("krit"), "zauberkrit": w.get("zkrit"), "ausweichen": w.get("ausw"),
                    "parieren": w.get("parier"), "ruestung": w.get("ruestung"), "leben": w.get("lp"), "mana": w.get("mana"),
                    "zaubermacht": w.get("zm"), "heilung": w.get("heil"), "treffer": w.get("treffer"),
                    "regen": w.get("regen"), "verteidigung": w.get("vert"), "umrechnung": leer(w.get("um")),
                    "anlass": w.get("warum"), "testlog": "4.0"})
    return out


def zusammen(name, neu, schluessel):
    pfad = os.path.join(D, name + ".csv")
    alt = at._read(pfad) if os.path.exists(pfad) else []
    key = lambda r: tuple(str(r.get(k, "")) for k in schluessel)
    m = {key(r): r for r in alt}
    for r in neu:
        m[key(r)] = {k: ("" if r.get(k) is None else r.get(k)) for k in F[name]}
    rows = list(m.values())
    at._write(pfad, F[name], rows)
    return rows


# --- Fischglas gegen Lagerstuhl ------------------------------------------------------------------------------------------------
def lager(w, profile):
    """Was +8 % Grundwerte (Fischglas) und +2 % Krit (Lagerstuhl) bringen: in Spielwerten (Umrechnung des Clients) und mit
    RXP-Gewichten. w = Stand aus werteLog (Testlog 4.0)."""
    e = {k: eff(w, k) for k in WERTE}
    um = kv(str(w.get("um") or "").replace(" ", ";"))
    d = {k: GLAS * v for k, v in e.items() if v}

    def je(name, stat):   # was ein Punkt mehr bringt: aus «…10» (Unterschied für 10 Punkte), sonst Verhältnis
        if um.get(name + "10") is not None:
            return float(um[name + "10"]) / 10
        if um.get(name) is not None and e.get(stat):
            return float(um[name]) / e[stat]
        return None
    spiel = {
        "AP": sum(d.get(s, 0) * (je(n, s) or 0) for n, s in (("apStae", "str"), ("apBew", "agi"))),
        "Krit %": d.get("agi", 0) * (je("kritBew", "agi") or 0),
        "Zauberkrit %": d.get("int", 0) * (je("zkritInt", "int") or 0),
        "Ausweichen %": d.get("agi", 0) * ((float(um["auswBew"]) / e["agi"]) if um.get("auswBew") is not None and e.get("agi") else 0),
        "Leben": d.get("sta", 0) * float(um.get("lpAus") or 0),
        "Mana": d.get("int", 0) * MANA_JE_INT,
        "Mana pro s aus Willenskraft": GLAS * float(um["manaWil"]) if um.get("manaWil") is not None else None,
    }
    bewertet = {}
    for spec, p in profile.items():
        if not p:
            continue
        glas = GLAS * sum(float(p.get(STAT_KEY[k]) or 0) * v for k, v in e.items() if v)
        stuhl = STUHL * (float(p.get("ITEM_MOD_CRIT_RATING_SHORT") or 0) + float(p.get("ITEM_MOD_CRIT_SPELL_RATING_SHORT") or 0))
        bewertet[spec] = (glas, stuhl, p.get("profil"))
    return d, spiel, bewertet


# --- Bericht -------------------------------------------------------------------------------------------------------------------
def _f(v, n=1):
    z = zahl(v)
    return "–" if z is None or z == "" else f"{z:.{n}f}"


def bericht(kampf, zauber, werte, daten):
    gew = gewichte()
    L = ["# Kampfdaten: Schaden, Zauber, Werte, Ausrüstung (erzeugt von `tools/kampf_aus_testlog.py`)", "",
         "Nicht von Hand ändern: neues Testlog einlesen und neu erzeugen. Ohne Charakternamen und Uhrzeiten.", "",
         "## Quellen", "",
         "- Testlog 4.0 (Forever-UI 1.60.1, Build 70450, https://github.com/Gethe/wow-ui-source/tree/forever): Schaden, Heilung "
         "und erlittener Schaden pro Zauber aus Blizzards Schadensmesser `C_DamageMeter` (nach dem Kampf gelesen, im Kampf "
         "«secret»); Treffer, Krits und Ausweichen am Spieler aus `UNIT_COMBAT`; Zauber mit Zeit aus `UNIT_SPELLCAST_SUCCEEDED`; "
         "Nahkampfschläge aus `PLAYER_SWING`; Werte aus `UnitStat` und Co. mit der Umrechnung des Charakterfensters "
         "(`GetCritChanceFromStat`, `GetAttackPowerForStat`, `Camelot/PaperDollFrameStats.lua`); Ausrüstung aus "
         "`GetInventoryItemLink` und `C_Item.GetItemStats`; Talente aus `C_Traits`.",
         f"- Gewichte für Gegenstände und Lagerbuffs: {QUELLE_RXP}; RXPs Zahlen fürs Leveln (Speedrun), kein Messwert.",
         "- Fischglas «8% increased stats», Lagerstuhl «2% increased critical strike chance with all spells and attacks» "
         "(Tooltips, https://metaforge.app/wow-forever/database/consumables/fish-bowl und …/camp-chair, abgerufen 17.10.2026). "
         "Gerechnet wird mit den fünf Grundwerten (Lesart; der Tooltip nennt sie nicht einzeln).",
         f"- Mana aus Intellekt: {MANA_JE_INT} je Punkt laut Warcraft Tavern (Forever, https://www.warcrafttavern.com/forever/guides/stats/).",
         "- Grenzen: Ohne Schadensmesser (Funktion fehlt, keine neue Sitzung, Werte geheim) steht der eigene Schaden nur als "
         "Schätzung aus den Treffern am Ziel (allein, ohne Gruppe). Prozent-Effekte von Gegenständen (Krit, Treffer) liefert "
         "`GetItemStats` vielleicht nicht; das Testlog hält dafür die Tooltip-Zeilen fest, die Muster für den deutschen Text "
         "sind eine Annahme.", ""]
    # Überblick
    grp = defaultdict(list)
    for r in kampf:
        grp[(r["klasse"], zahl(r["stufe"]) or 0, r["gestalt"])].append(r)
    L += ["## Überblick pro Stufe und Gestalt", "",
          "| Klasse | Stufe | Gestalt | Kämpfe | Ø Dauer | Schaden pro s (Messer) | Heilung | erlitten pro s | Krit am Spieler | "
          "vermieden | Krit am Ziel (allein) | Tode |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for (kl, st, ge), rs in sorted(grp.items(), key=lambda x: (x[0][0], x[0][1], str(x[0][2]))):
        dauer = sum(float(r["dauer_s"] or 0) for r in rs)
        mit = [r for r in rs if str(r["schaden"]).strip()]
        dps = sum(float(r["schaden"]) for r in mit) / max(1e-9, sum(float(r["dauer_s"] or 0) for r in mit)) if mit else None
        hei = sum(float(r["heilung"] or 0) for r in rs if str(r["heilung"]).strip())
        erl = sum(float(r["erlitten"] or 0) for r in rs)
        tr = sum(int(float(r["erlitten_treffer"] or 0)) for r in rs)
        kr = sum(int(float(r["erlitten_krit"] or 0)) for r in rs)
        verm = Counter()
        for r in rs:
            for t in str(r["vermieden"] or "").split():
                if ":" in t:
                    verm[t.split(":")[0]] += int(float(t.split(":")[1]))
        vg = sum(verm.values())
        zt = sum(int(float(r["am_ziel_treffer"] or 0)) for r in rs if str(r["am_ziel_treffer"]).strip())
        zk = sum(int(float(r["am_ziel_krit"] or 0)) for r in rs if str(r["am_ziel_krit"]).strip())
        L.append(f"| {KLASSE_DE.get(kl, kl)} | {st} | {ge} | {len(rs)} | {dauer / len(rs):.1f} s | "
                 f"{'–' if dps is None else f'{dps:.1f}'} | {hei:.0f} | {erl / max(1e-9, dauer):.1f} | "
                 f"{(100 * kr / tr) if tr else 0:.0f} % von {tr} | "
                 f"{', '.join(f'{n} {AUSW_DE.get(a, a)}' for a, n in verm.most_common()) or '–'} ({(100 * vg / (vg + tr)) if vg + tr else 0:.0f} %) | "
                 f"{(100 * zk / zt) if zt else 0:.0f} % von {zt} | {sum(1 for r in rs if r['tod'])} |")
    if not kampf:
        L.append("| – | | | 0 | | | | | | | | |")
    # Zauber
    nach_k = {r["kennung"]: r for r in kampf}
    zg = defaultdict(lambda: defaultdict(lambda: {"anzahl": 0, "schaden": 0, "heilung": 0}))
    zeit = defaultdict(float)
    for r in kampf:
        zeit[(r["klasse"], r["gestalt"])] += float(r["dauer_s"] or 0)
    for z in zauber:
        r = nach_k.get(z["kennung"])
        if not r:
            continue
        e = zg[(r["klasse"], r["gestalt"])][z["zauber"]]
        e["name"] = z.get("name") or e.get("name") or ""
        e["anzahl"] += int(float(z["anzahl"] or 0))
        e["schaden"] += float(z["schaden"] or 0)
        e["heilung"] += float(z["heilung"] or 0)
    L += ["", "## Zauber pro Gestalt (Anzahl, pro Minute, Anteil am Schaden laut Schadensmesser)", ""]
    for (kl, ge), zs in sorted(zg.items(), key=lambda x: (x[0][0], str(x[0][1]))):
        summe = sum(e["schaden"] for e in zs.values()) or 0
        L += [f"**{KLASSE_DE.get(kl, kl)}, {ge}** ({zeit[(kl, ge)] / 60:.1f} Minuten im Kampf)", "",
              "| Zauber | Anzahl | pro Minute | Schaden | Anteil | Heilung |", "|---|---|---|---|---|---|"]
        for sid, e in sorted(zs.items(), key=lambda x: (-x[1]["schaden"], -x[1]["anzahl"]))[:12]:
            L.append(f"| {e['name'] or '?'} ({sid}) | {e['anzahl']} | {e['anzahl'] / max(1e-9, zeit[(kl, ge)] / 60):.1f} | "
                     f"{e['schaden']:.0f} | {(100 * e['schaden'] / summe) if summe else 0:.0f} % | {e['heilung']:.0f} |")
        L.append("")
    if not zg:
        L += ["Noch keine Kämpfe mit Zaubern.", ""]
    # Eröffnung und Abstände
    L += ["## Eröffnung und Abstände zwischen Zaubern", "",
          "Die ersten drei Zauber jedes Kampfes (negative Zeit: vor dem Kampfbeginn) und der mittlere Abstand zwischen zwei Zaubern.", "",
          "| Klasse | Gestalt | häufigste Eröffnungen | Kämpfe | mittlerer Abstand |", "|---|---|---|---|---|"]
    er = defaultdict(Counter)
    ab = defaultdict(list)
    for r in kampf:
        folge = [x.split("@") for x in str(r.get("folge") or "").replace(" ", ",").split(",") if "@" in x]
        if not folge:
            continue
        ids = [daten["zauber"].get(zahl(i), str(i)) for i, _ in folge[:3]]
        er[(r["klasse"], r["gestalt"])][" → ".join(ids)] += 1
        zs = [float(t) for _, t in folge]
        ab[(r["klasse"], r["gestalt"])] += [b - a for a, b in zip(zs, zs[1:]) if b >= a]
    for key, c in sorted(er.items(), key=lambda x: (x[0][0], str(x[0][1]))):
        top = "; ".join(f"{t} ({n}×)" for t, n in c.most_common(3))
        med = statistics.median(ab[key]) if ab[key] else None
        L.append(f"| {KLASSE_DE.get(key[0], key[0])} | {key[1]} | {top} | {sum(c.values())} | "
                 f"{'–' if med is None else f'{med:.1f} s'} |")
    if not er:
        L.append("| – | | | 0 | |")
    # Erlittene Treffer pro Gegner
    pg = defaultdict(lambda: {"n": 0, "treffer": 0, "summe": 0.0, "krit": 0})
    for r in kampf:
        gegner = [t.split(":")[0] for t in str(r["gegner"] or "").split() if t]
        if len(gegner) != 1:
            continue   # nur Kämpfe gegen genau einen Gegner: sonst lässt sich der Schaden nicht zuordnen
        e = pg[(gegner[0], r["gestalt"])]
        e["n"] += 1
        e["treffer"] += int(float(r["erlitten_treffer"] or 0))
        e["summe"] += float(r["erlitten"] or 0)
        e["krit"] += int(float(r["erlitten_krit"] or 0))
    L += ["", "## Erlittene Treffer pro Gegner (Kämpfe gegen genau einen Gegner)", "",
          "| Kreatur | Gestalt | Kämpfe | Treffer | Ø Schaden pro Treffer | Krit |", "|---|---|---|---|---|---|"]
    for (cr, ge), e in sorted(pg.items(), key=lambda x: -x[1]["n"])[:20]:
        L.append(f"| {cr} | {ge} | {e['n']} | {e['treffer']} | {(e['summe'] / e['treffer']) if e['treffer'] else 0:.1f} | "
                 f"{(100 * e['krit'] / e['treffer']) if e['treffer'] else 0:.0f} % |")
    if not pg:
        L.append("| – | | 0 | | | |")
    # Werte
    L += ["", "## Werte (neuester Stand pro Stufe und Gestalt)", "",
          "| Klasse | Stufe | Gestalt | Stä | Bew | Aus | Int | Wil | AP | Krit | Zauberkrit | Ausweichen | Rüstung | Leben | Mana | Umrechnung |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for w in werte:
        L.append(f"| {KLASSE_DE.get(w['klasse'], w['klasse'])} | {w['stufe']} | {w['gestalt']} | {w['str']} | {w['agi']} | "
                 f"{w['sta']} | {w['int']} | {w['spi']} | {w['ap']} | {w['krit']} | {w['zauberkrit']} | {w['ausweichen']} | "
                 f"{w['ruestung']} | {w['leben']} | {w['mana']} | {w['umrechnung']} |")
    if not werte:
        L.append("| – | | | | | | | | | | | | | | | |")
    # Fischglas gegen Lagerstuhl
    L += ["", "## Fischglas (+8 % Grundwerte) gegen Lagerstuhl (+2 % Krit)", "",
          "Mit dem neuesten Stand der Werte. «Spielwerte»: was die 8 % laut Umrechnung des Clients bringen. «RXP»: beide Buffs "
          "mit RXPs Gewichten in Punkten (Lagerstuhl = 2 × Gewicht für 1 % Krit, Nahkampf und Zauber zusammen, weil Forever "
          "beide Krit-Werte zusammenlegt; Fischglas = 8 % der gewichteten Grundwerte). Pro Spieler gibt es nur einen "
          "Lager-Gegenstand pro Stunde (gemeinsame Abklingzeit, wow-professions Camping Guide).", ""]
    neu = {}
    for (kl, lvl, form), w in daten["werte"].items():
        if (kl, form) not in neu or (neu[(kl, form)][0] or 0) < (lvl or 0):
            neu[(kl, form)] = (lvl, w)
    for (kl, form), (lvl, w) in sorted(neu.items(), key=lambda x: (x[0][0], str(x[0][1]))):
        profile = {s: profil(gew, kl, lvl, s) for s in specs(gew, kl)}
        d, spiel, bew = lager(w, profile)
        L.append(f"**{KLASSE_DE.get(kl, kl)}, Stufe {lvl}, {form}:** Fischglas +" +
                 ", ".join(f"{v:.1f} {WERTE_DE[k]}" for k, v in d.items()) + " → " +
                 ", ".join(f"{k} +{v:.2f}" if k.endswith("%") else f"{k} +{v:.1f}" for k, v in spiel.items()
                           if v is not None and v > 0) + "; Lagerstuhl: Krit +2 %, Zauberkrit +2 %.")
        for spec, (g, s, name) in sorted(bew.items()):
            L.append(f"- RXP «{name}»: Fischglas {g:.1f}, Lagerstuhl {s:.1f} Punkte"
                     + (f" (Glas {g / s:.1f}-mal so viel)" if s and g >= s else (f" (Stuhl {s / g:.1f}-mal so viel)" if g else "")))
        L.append("")
    if not neu:
        L += ["Noch keine Werte im Testlog (ab Testlog 4.0, ausserhalb des Kampfes).", ""]
    # Ausrüstung
    L += ["## Ausrüstung (neuester Stand pro Charakter)", ""]
    for ch, c in sorted(daten["chars"].items(), key=lambda x: (x[1].get("klasse") or "", -(x[1].get("stufe") or 0))):
        aus = c.get("ausruestung") or {}
        if not aus:
            continue
        kl, lvl = c.get("klasse"), c.get("stufe") or 0
        sp = specs(gew, kl)
        L += [f"**{KLASSE_DE.get(kl, kl)}, Stufe {lvl}**", "",
              "| Platz | Gegenstand | Werte | " + " | ".join(f"RXP {s}" for s in sp) + " |",
              "|---|---|---|" + "---|" * len(sp)]
        summe = defaultdict(float)
        for slot in sorted(int(s) for s in aus):
            e = aus.get(slot) or aus.get(str(slot)) or {}
            if not isinstance(e, dict) or not e.get("k"):
                continue
            stats, aus_text, _ = item_stats(daten, e.get("k"))
            iid = (re.match(r"item:(\d+)", e["k"]) or [None, "?"])[1]
            werte_p = []
            for s in sp:
                p = punkte(stats, profil(gew, kl, lvl, s))
                summe[s] += p or 0
                werte_p.append("–" if p is None else f"{p:.1f}")
            L.append(f"| {SLOTS[slot - 1] if 0 < slot <= len(SLOTS) else slot} | {e.get('n') or '?'} ({iid}) | "
                     f"{stats_text(stats, aus_text)} | " + " | ".join(werte_p) + " |")
        L.append("| **Summe** | | | " + " | ".join(f"{summe[s]:.1f}" for s in sp) + " |")
        L.append("")
    # Belohnungen
    L += ["## Quest-Belohnungen zur Wahl", "",
          "Punkte mit RXPs Gewichten für die Stufe beim Abgeben; «gewählt» laut Testlog.", ""]
    zeilen = 0
    for ch, c in daten["chars"].items():
        kl = c.get("klasse")
        sp = specs(gew, kl)
        for _, b in sorted((c.get("belohnungen") or {}).items(), key=lambda x: zahl(x[1].get("t")) or 0):
            lvl = zahl(b.get("lvl")) or 0
            teile = []
            for i, iid in enumerate(str(b.get("items") or "").split(","), 1):
                stats, aus_text, _ = item_stats(daten, item_id=zahl(iid))
                namen = str(b.get("namen") or "").split(" / ")
                name = (daten["info"].get(zahl(iid)) or {}).get("n") or (namen[i - 1] if i <= len(namen) and namen[i - 1] else "?")
                pts = ", ".join(f"{s} {punkte(stats, profil(gew, kl, lvl, s)) or 0:.1f}" for s in sp)
                teile.append(f"{i}) {name} ({iid}): {stats_text(stats, aus_text)}" + (f" [{pts}]" if pts else ""))
            wahl = zahl(b.get("wahl"))
            L.append(f"- Quest {b.get('q') or '?'}, Stufe {lvl}, {KLASSE_DE.get(kl, kl)}: " + " · ".join(teile)
                     + (f" — gewählt {wahl}" if wahl else " — nicht gewählt"))
            zeilen += 1
    if not zeilen:
        L.append("Noch keine Quest mit Belohnungen zur Wahl im Testlog (ab Testlog 4.0).")
    # Talente
    L += ["", "## Talente (neuester Stand pro Charakter)", ""]
    n_t = 0
    for ch, c in daten["chars"].items():
        t = c.get("talente")
        if isinstance(t, dict) and t.get("liste"):
            L.append(f"- {KLASSE_DE.get(c.get('klasse'), c.get('klasse'))}, Stufe {zahl(t.get('lvl')) or '?'}: "
                     f"{t.get('punkte') or ''} — {t.get('liste')}")
            n_t += 1
    if not n_t:
        L.append("Noch keine Talente im Testlog (ab Testlog 4.0).")
    L.append("")
    os.makedirs(os.path.dirname(BERICHT), exist_ok=True)
    open(BERICHT, "w", encoding="utf-8").write("\n".join(L))


def main():
    args = sys.argv[1:]
    if args and args[0] == "--gewichte":
        pfad = args[1] if len(args) > 1 else RXP_WEIGHTS
        print(f"{gewichte_schreiben(pfad)} Profile nach {os.path.relpath(GEWICHTE, ROOT)}")
        return
    pfade = [a for a in args if not a.startswith("--")]
    if not pfade:
        raise SystemExit(USAGE)
    daten = lade(pfade)
    os.makedirs(D, exist_ok=True)
    k = zusammen("kampf", kampf_zeilen(daten), ["kennung"])
    z = zusammen("kampf_zauber", zauber_zeilen(daten), ["kennung", "zauber"])
    w = zusammen("werte", werte_zeilen(daten), ["klasse", "stufe", "gestalt"])
    bericht(k, z, w, daten)
    print(f"{len(daten['kampf'])} Kämpfe, {len(daten['werte'])} Werte-Stände, {len(daten['chars'])} Charaktere; "
          f"Bericht: {os.path.relpath(BERICHT, ROOT)}")


if __name__ == "__main__":
    main()
