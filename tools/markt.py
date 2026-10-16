# Empfehlungen aus dem Testlog (ab Version 3.6) und den eigenen AH-Preisen: was herstellen, was kaufen und wieder
# verkaufen, was aus dem Bestand verkaufen, was farmen. Das Werkzeug rechnet nur; kaufen, einstellen und entscheiden
# tut der Spieler.
#
# Aufruf:  python3 tools/markt.py <KombiTestlog.lua> [--marge 0.3] [--aus <Ordner>]
#
# Liest die SavedVariables-Datei des Testlogs (Rezepte, Bestand, AH-Post, AH-Scans, Gegenstands-Infos, Protokoll), dazu
# aus dem Repo data/preise/ah_eigen.csv und ah_abnahme.csv (Verlauf früherer Scans, geschrieben von
# tools/ah_aus_testlog.py) und die Händlerpreise aus data/kombi/preise_zusatz.csv und data/rechnung/Preise.csv.
# Schreibt nur nach build/markt/ (nicht versioniert: Bericht und Daten enthalten den eigenen Bestand und eigene Verkäufe):
#   markt.md                   Bericht mit Quellen, Rechenweg, Tabellen und Grenzen
#   KombiDaten/KombiDaten.toc  Addon fürs Spiel. Der Ordner gehört nach Interface\AddOns\KombiDaten, nie in einen der
#   KombiDaten/Daten.lua       mit dem Repo verknüpften Addon-Ordner. Im Spiel zeigt /tl tipp die Empfehlungen.
#
# Rechenweg (Preise in Kupfer):
#   Verkaufspreis  kleinerer Wert aus dem Tiefstpreis jetzt und dem Median der Tiefstpreise der letzten 7 Tage
#                  (vollständige Scans, gleicher Markt, mindestens MIN_SCANS Scans an MIN_TAGE Tagen), abzüglich 5 %
#                  Gebühr (AHledger, Seite «Auction House»: https://ahledger.com/wow-forever/auction-house). Ohne
#                  genug Verlauf: Tiefstpreis jetzt, «kurzer Verlauf», nur im Bericht, nicht in den Tipps.
#   Herstellen     Wert des Ergebnisses (mittlere Menge) gegen die Reagenzien zum Einkaufspreis (Händlerpreis, sonst die
#                  billigsten Angebote des letzten Scans).
#   Kaufen und wieder verkaufen
#                  Angebote des letzten Scans unter (Tiefstpreis 7 Tage × 0,95) / (1 + Marge). Menge höchstens: was in den
#                  beobachteten Stunden geschätzt gekauft wurde (nie hochgerechnet, höchstens auf 72 Stunden umgelegt),
#                  oder was du selbst in den letzten 72 Stunden verkauft hast. Abnahme zählt erst ab MIN_VERGLEICHE
#                  Vergleichen über MIN_STUNDEN Stunden. Ohne Beleg keine Empfehlung.
#   Pfand          geht bei Nichtverkauf verloren; die Höhe kennt das Werkzeug nur aus eigenen Angeboten (AH-ANGEBOT).
#   Abnahme        eine Schätzung (Testlog 3.6, data/preise/ah_abnahme.csv): zu hoch, wenn jemand zurückzieht und teurer
#                  neu einstellt; zu tief, wenn neue Angebote dazukommen.
#   Langzeit       Median der Tiefstpreise und Abnahme der letzten 30 Tage, nur als Vergleich (Beleg-Text, Spalte im
#                  Bericht) und als Warnung, wenn der 7-Tage-Wert 20 % oder mehr darüber liegt. Preis, Beleg und Menge
#                  bleiben bei 7 Tagen.
#   Farmen         Wert pro Stunde aus ANGELN, SAMMELN und BEUTE; ein Tipp erst ab 15 Minuten und nur, wenn jede Beute
#                  einen Preis hat (AH mit Verlauf oder Händlerpreis aus den Gegenstands-Infos, Testlog 3.6).
#   Für den Händler herstellen (seit 15.10.)
#                  Rezepte, deren Ergebnis der Händler höher bezahlt (Forever-Client: Gegenstands-Infos, AH-Scan 3.7,
#                  data/preise/haendler_ankauf.csv), als das Material im letzten Scan kostet (Preisstufen, Händlerware zum
#                  Händlerpreis). Seit 16.10.: alle Tipps teilen ein Angebotsbuch (was ein Rezept kauft, fehlt dem nächsten),
#                  Herstellung um Herstellung geht an das Rezept mit dem grössten Gewinn, mindestens HAENDLER_MIN_STK je Stück;
#                  Zwischenprodukte, die der Charakter selbst herstellen kann, und Geringe Essenzen aus geteilten Grossen
#                  (ESSENZEN) nur, wenn das billiger ist. Ohne AH-Gebühr und ohne Absatz-Risiko; der Preis gilt aber nur,
#                  solange die Angebote liegen (Grenzpreis im Tipp).
#   Essenzen       Geringe Essenz = ein Drittel einer Grossen (gemessen 13.10. für die Magieessenz: aus 9 wurden 27), wenn
#                  das billiger ist; gilt für Einkauf, Herstellen und den nächsten Schritt.
#   Sammler (seit 16.10.)
#                  Nächster Schritt für Charaktere mit Kürschnerei oder Kräuterkunde und ohne Lederverarbeitung und
#                  Verzauberkunst (Berufe und Geld aus chars ab Testlog 3.7.1, sonst aus den Zeilen BERUF und GELD nach der
#                  letzten SITZUNG des Charakters): Material für Stufe A behalten, Gold für den Wechsel in Orgrimmar, Beute,
#                  die im AH ein Vielfaches des Händlerpreises bringt (ohne Absatz-Beleg).
#   Für das Testlog (seit 16.10.)
#                  KombiDaten.nichtVerkaufen (Warnung beim Händler, Testlog 3.7.1) und KombiDaten.beobachten (zusätzliche
#                  Gegenstände mit Preisstufen und Abnahme im AH-Scan).
#   Unter Händlerpreis
#                  Angebote, die weniger kosten, als der Händler zahlt (Testlog 3.7 zählt sie beim Scan; ältere Scans: nur
#                  Gegenstände mit Preisstufen und bekanntem Händlerpreis).
#   Nächster Schritt (pro Charakter, im Spiel /tl tipp)
#                  Berufe: der Abschnitt des Berufe-Plans (tools/plan_berufe.py) für die jetzige Fertigkeit, was dafür fehlt
#                  und was es im AH kostet, ob das Rezept noch zu lernen ist (data/kombi/lehrer.csv); Verzauberkunst: das
#                  billigste Rezept, das schon geht, mit dem Zauberstab-Weg als Vergleich; Material des Plans, das der
#                  Charakter nicht mehr braucht (Überschuss).
import math, os, re, statistics, sys
from collections import defaultdict
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ah_aus_testlog as at

AUS = os.path.join(at.ROOT, "build", "markt")
GEBUEHR = 0.05      # AHledger, Seite «Auction House» (Best Practice §9)
MARGE = 0.30        # Mindestmarge für «kaufen und wieder verkaufen» (Wahl von Claude, mit --marge änderbar)
ABSATZ_STUNDEN = 72 # Kaufmenge höchstens: geschätzte Abnahme, auf so viele Stunden umgelegt (nie hochgerechnet)
MIN_VERGLEICHE = 2  # Abnahme aus Scans zählt als Beleg ab so vielen Vergleichen …
MIN_STUNDEN = 1.0   # … über mindestens so viele beobachtete Stunden
MIN_SCANS = 3       # Verlauf gilt ab so vielen vollständigen Scans in 7 Tagen …
MIN_TAGE = 2        # … an so vielen verschiedenen Tagen
LANGZEIT_TAGE = 30  # Langzeit-Vergleich: Tiefstpreis und Abnahme der letzten 30 Tage (Anzeige und Warnung)
LANGZEIT_WARNUNG = 0.20  # Warnung, wenn der 7-Tage-Tiefstpreis so weit über dem 30-Tage-Wert liegt (Wahl von Claude)
MAX_TIPPS = 12
BOUT_PAUSE = 600    # Sekunden ohne Fang oder Beute: neuer Durchgang (Farmen pro Stunde)
MIN_EREIGNISSE = 5  # Durchgänge mit weniger Ereignissen zählen nicht
MIN_FARM_STUNDEN = 0.25  # Farm-Tipp erst ab so vielen beobachteten Stunden und nur, wenn jede Beute einen Preis hat
                         # (Wahl von Claude)
FARBE = {0: "orange", 1: "gelb", 2: "grün", 3: "grau"}
HAENDLER_MIN_GEWINN = 20   # Kupfer: kleinere Gewinne beim Herstellen für den Händler sind kein Tipp (Wahl von Claude)
HAENDLER_MIN_STK = 5       # Kupfer je Herstellung: darunter zählt eine weitere Herstellung nicht mehr (Wahl von Claude, 16.10.)
# Geringe -> Grosse Essenz (Item-IDs aus dem eigenen Scan, data/preise/ah_alle.csv). 1 Grosse = 3 Geringe: gemessen für die
# Magieessenz (Testlog 13.10., aus 9 wurden 27, docs/tests/messdaten-2026-10-13.md); die übrigen wie in Classic (Tooltip
# «Turn a greater … essence into three lesser ones», https://github.com/nexus-devs/wow-classic-items), in Forever ungeprüft.
ESSENZEN = {10938: 10939, 10998: 11082, 11134: 11135, 11174: 11175, 16202: 16203}
STUFE_A = {2934: 99, 2318: 62, 783: 27}   # Material für Stufe A in Orgrimmar (docs/plan/berufe-plan.md, Sweetspot): Fetzen,
                                          # Leichtes Leder, Leichter Balg
PLAN_LEDER = (2934, 2318, 783, 2319, 4232)   # Leder und Bälge des Plans: nie zum Händler (Liste für das Testlog)
VIELFACH = 3        # Beute mit AH-Wert (nach Gebühr) mindestens so viel mal über dem Händlerpreis: AH statt Händler (Wahl
                    # von Claude, ohne Absatz-Beleg; Vorschlag der Markt-Analyse vom 16.10.)
MIN_ANGEBOT = 20    # … und mindestens so viele Stück im Angebot (sonst ist der Preis Zufall)
WARN_MAX = 300      # Einträge in KombiDaten.nichtVerkaufen höchstens
ANKAUF_CSV = os.path.join(at.D, "preise", "haendler_ankauf.csv")
LEHRER_CSV = os.path.join(at.D, "kombi", "lehrer.csv")
BERUF_KURZ = {"Lederverarbeitung": "LW", "Verzauberkunst": "VZ"}
INTERFACE = "16001" # wie die anderen Addons (Forever-Client 1.60.1)
USAGE = "Aufruf: python3 tools/markt.py <KombiTestlog.lua> [--marge 0.3] [--aus <Ordner>]"


def geld(c):
    """Kupfer -> «1g 2s 3c»."""
    if c is None:
        return "–"
    neg = c < 0
    s = at.silber(abs(c) / 100)
    return ("-" if neg else "") + s


def prozent(x):
    return "–" if x is None else f"{x * 100:.0f} %"


# --- Lesen ---------------------------------------------------------------------------------------------------------------
def lade(text):
    if not at.ist_datei(text):
        raise SystemExit("Bitte die Datei KombiTestlog.lua (SavedVariables) angeben; der Text von /tl zeigen reicht hier nicht.")
    db = at._py(at._lua_tabelle(text))
    scans = at._aus_lua(db)
    namen = at.namen_aus_db(db)
    for s in scans:
        s["namen"] = namen
    return db, scans, namen


def liste(text):
    """«ID:Anzahl;…» -> {ID: Anzahl}."""
    out = {}
    for teil in (text or "").split(";"):
        f = teil.split(":")
        if len(f) == 2 and f[0].isdigit():
            out[int(f[0])] = out.get(int(f[0]), 0) + int(float(f[1]))
    return out


def rezepte(text):
    """«Rezept:Ergebnis:min:max:Farbe:Reagenzien;…» -> [dict]."""
    out = []
    for teil in (text or "").split(";"):
        f = teil.split(":")
        if len(f) != 6:
            continue
        reag = []
        for r in f[5].split(","):
            if "*" in r:
                i, n = r.split("*")
                reag.append((int(i), int(float(n))))
        out.append({"id": int(f[0]), "out": int(f[1]) or None, "qmin": int(f[2]), "qmax": int(f[3]),
                    "farbe": None if f[4] == "-" else int(f[4]), "reag": reag})
    return out


def punkte(scans, markt):
    """Item-ID -> [(datum, Tiefstpreis, Median, Menge)] aus vollständigen Scans dieses Markts: data/preise/ah_eigen.csv
    (beobachtete Gegenstände, alle früheren Scans) und die Scans der Datei (alle Gegenstände)."""
    out = defaultdict(dict)
    if os.path.exists(at.EIGEN):
        for r in at._read(at.EIGEN):
            if r["markt"] == markt and r.get("hinweis") != "unvollständig" and r.get("tiefstpreis_s"):
                out[int(r["item_id"])][r["datum"]] = (round(float(r["tiefstpreis_s"]) * 100),
                                                      round(float(r["median_s"] or r["tiefstpreis_s"]) * 100),
                                                      int(float(r["menge"] or 0)))
    for s in scans:
        if f"{s['markt']} {s['phase']}" != markt or s["unvollstaendig"]:
            continue
        for i, p in s["preise"].items():
            out[i][s["datum"]] = (p["tiefst"], p["median"], p["menge"])
    return {i: sorted((d,) + v for d, v in m.items()) for i, m in out.items()}


def kennzahlen(pkt, bis):
    """7-Tage- und 30-Tage-Werte bis zum letzten Scan: Median der Tiefstpreise, Anzahl Scans und Tage, Menge, Trend."""
    ende = datetime.strptime(bis, "%Y-%m-%d %H:%M")
    def fenster(tage, ab=0):
        von = (ende - timedelta(days=tage)).strftime("%Y-%m-%d %H:%M")
        bis_ = (ende - timedelta(days=ab)).strftime("%Y-%m-%d %H:%M")
        return [p for p in pkt if von <= p[0] <= bis_]
    w7, w30 = fenster(7), fenster(30)
    k = {"n7": len(w7), "tage7": len({p[0][:10] for p in w7}), "n30": len(w30), "tage30": len({p[0][:10] for p in w30}),
         "boden7": statistics.median(p[1] for p in w7) if w7 else None,
         "boden30": statistics.median(p[1] for p in w30) if w30 else None,
         "menge7": statistics.median(p[3] for p in w7) if w7 else None}
    neu, alt = fenster(3), [p for p in w7 if p not in fenster(3)]
    k["trend"] = None
    if neu and alt:
        a = statistics.median(p[1] for p in alt)
        if a > 0:
            k["trend"] = statistics.median(p[1] for p in neu) / a - 1
    k["verlauf"] = k["n7"] >= MIN_SCANS and k["tage7"] >= MIN_TAGE
    return k


def haendlerpreise(plan):
    """Item-ID -> Händlerpreis in Kupfer (Einkauf beim Händler) aus den Plan-Tabellen."""
    out = {}
    for i, e in plan.items():
        if e.get("haendler") and e.get("plan_s") is not None:
            out[i] = round(e["plan_s"] * 100)
    return out


def ankaufpreise(db, jetzt):
    """Item-ID -> Kupfer, was der Händler im Forever-Client zahlt: Händlerpreis im letzten AH-Scan (Testlog 3.7), sonst
    die Gegenstands-Infos dieser Datei (Testlog 3.6), sonst data/preise/haendler_ankauf.csv (frühere Testlogs)."""
    out = {}
    if os.path.exists(ANKAUF_CSV):
        for r in at._read(ANKAUF_CSV):
            if r["item_id"].isdigit() and (r.get("ankauf_kupfer") or "").strip():
                out[int(r["item_id"])] = int(float(r["ankauf_kupfer"]))
    for k, v in als_dict(db.get("info")).items():
        if str(k).isdigit() and isinstance(v, dict) and v.get("s") is not None:
            out[int(k)] = int(v["s"])
    for i, p in (jetzt or {}).items():
        if p.get("haendler") is not None:
            out[i] = p["haendler"]
    return out


def als_dict(x):
    """Lua-Tabelle aus at._py: Listen (Schlüssel 1..n) wieder als dict."""
    if isinstance(x, list):
        return {i + 1: v for i, v in enumerate(x)}
    return x if isinstance(x, dict) else {}


# --- Markt ---------------------------------------------------------------------------------------------------------------
class Markt:
    def __init__(self, db, scans, namen, marge=MARGE):
        self.db, self.namen, self.marge = db, namen, marge
        self.plan = at.plan_items()
        self.info = {int(k): v for k, v in als_dict(db.get("info")).items() if str(k).isdigit() and isinstance(v, dict)}
        voll = [s for s in scans if not s["unvollstaendig"]]
        self.letzter = max(voll or scans, key=lambda s: (s["datum"], s["zeit"])) if scans else None
        self.markt = f"{self.letzter['markt']} {self.letzter['phase']}" if self.letzter else None
        self.scans = [s for s in scans if f"{s['markt']} {s['phase']}" == self.markt]
        self.jetzt = self.letzter["preise"] if self.letzter else {}
        self.pkt = punkte(scans, self.markt) if self.markt else {}
        self.kz = {i: kennzahlen(p, self.letzter["datum"]) for i, p in self.pkt.items()} if self.letzter else {}
        abn_rows, _ = at.zusammenfuehren_abnahme(at.zeilen_abnahme(scans))
        self.abn_rows = [r for r in abn_rows if r["markt"] == self.markt]
        self.abn = at.abnahme_summe(self.abn_rows, self.markt) if self.markt else {}
        self.abn30 = at.abnahme_summe(self.abn_rows, self.markt, tage=LANGZEIT_TAGE) if self.markt else {}
        self.haendler = haendlerpreise(self.plan)
        self.name2id = {}
        for i, n in namen.items():
            self.name2id.setdefault(n, i)
        self.eigen, self.gebuehr_eigen = self._eigene_verkaeufe()
        self.ankauf = ankaufpreise(db, self.jetzt)

    def name(self, i):
        p = self.plan.get(i, {})
        return self.namen.get(i) or (self.info.get(i) or {}).get("n") or p.get("deutsch") or p.get("material") or f"Item {i}"

    # Preise
    def verkauf(self, i):
        """(Kupfer pro Stück vor Gebühr, Herkunft, belastbar) oder (None, Grund, False)."""
        p, k = self.jetzt.get(i), self.kz.get(i)
        if k and k["verlauf"]:
            v = min(k["boden7"], p["tiefst"]) if p else k["boden7"]
            return v, f"7 Tage ({k['n7']} Scans, {k['tage7']} Tage)", True
        if p:
            return p["tiefst"], "nur letzter Scan", False
        return None, "kein Angebot im AH", False

    def netto(self, i):
        v, _, _ = self.verkauf(i)
        return None if v is None else v * (1 - GEBUEHR)

    def _ah(self, i, n, schon=0):
        """(Kupfer, Herkunft) für n Stück aus den billigsten Angeboten des letzten Scans, nachdem «schon» Stück weg sind
        (gemeinsames Angebotsbuch mehrerer Tipps); None ohne Angebot."""
        p = self.jetzt.get(i)
        if not p:
            return None
        if p.get("stufen"):
            k1, got1 = at.kosten(p["stufen"], schon + n)
            k0, got0 = at.kosten(p["stufen"], schon) if schon else (0, 0)
            k, got = k1 - k0, got1 - got0
            if got >= n:
                return k, "AH"
            letzt = p["stufen"][-1][0]
            if p["menge"] >= schon + n:
                return k + (n - got) * letzt, "AH (Rest geschätzt)"
            return k + (n - got) * letzt, f"AH, nur {p['menge']} im Angebot"
        return p["tiefst"] * n, "AH-Tiefstpreis"

    def einkauf_ex(self, i, n, buch=None):
        """(Kupfer für n Stück, Herkunft, {Item-ID: Stück aus dem AH}) – Händler, sonst die billigsten Angebote des letzten
        Scans nach dem, was «buch» schon verbraucht hat; Geringe Essenzen auch als Grosse gekauft und geteilt (ESSENZEN),
        wenn das billiger ist."""
        gemeinsam = buch is not None   # mit Angebotsbuch: Reste aus dem Teilen braucht die nächste Herstellung
        buch = buch or {}
        h = self.haendler.get(i)
        g = ESSENZEN.get(i)
        # Geringe, die beim Teilen übrig blieben (Schlüssel («rest», ID) im Angebotsbuch), zuerst; sie kosten nichts mehr
        r = min(buch.get(("rest", i), 0), n) if g else 0
        n2 = n - r
        if g and n2 == 0:
            return 0, "AH (Rest aus geteilter Grosser)", {("rest", i): -r}
        ah = self._ah(i, n2, buch.get(i, 0))
        wahl = (ah[0], ah[1], {i: n2, ("rest", i): -r} if r else {i: n2}) if ah else None
        if g:
            ng = math.ceil(n2 / 3)
            ag = self._ah(g, ng, buch.get(g, 0))
            # Mit Angebotsbuch zählt der Stückpreis (übrige Geringe aus dem Teilen braucht die nächste Herstellung, «rest»),
            # sonst der Preis für genau diese Menge
            billiger = (wahl is None or (ag[0] / (3 * ng) < wahl[0] / n2 if gemeinsam else ag[0] < wahl[0])) if ag else False
            if ag and not ag[1].startswith("AH, nur") and billiger:
                wahl = (ag[0], f"{ag[1]}, als {ng} {self.name(g)} gekauft und geteilt", {g: ng, ("rest", i): 3 * ng - n2 - r})
        if h is not None and (wahl is None or h * n <= wahl[0]):
            return h * n, "Händler", {}
        if wahl:
            return wahl
        k = self.kz.get(i)
        if k and k["verlauf"]:
            return k["boden7"] * n, "Tiefstpreis 7 Tage (jetzt nicht im Angebot)", {}
        return None, "kein Preis", {}

    def einkauf(self, i, n):
        """(Kupfer für n Stück, Herkunft) – wie einkauf_ex, ohne gemeinsames Angebotsbuch."""
        k, wo, _ = self.einkauf_ex(i, n)
        return k, wo

    # Abnahme und eigene Verkäufe
    def _eigene_verkaeufe(self):
        """Pro Item-ID: verkauft (Stück, Rechnungen, Erlös, davon in den 72 Stunden vor dem letzten Scan), abgelaufen,
        angeboten, Pfand. Eine vorläufige Rechnung zählt nicht, wenn die endgültige desselben Verkaufs da ist (gleicher
        Gegenstand, gleiche Menge und gleicher Preis, Brief bis 3 Stunden später angekommen)."""
        post = [r for r in als_dict(self.db.get("ahPost")).values() if isinstance(r, dict)]
        out = defaultdict(lambda: {"verkauft": 0, "verkauft_72h": 0, "erloes": 0, "n": 0, "abgelaufen": 0, "angeboten": 0,
                                   "pfand": 0, "pfand_stueck": 0})
        final = [r for r in post if r.get("art") == "verkauft" and not r.get("vorlaeufig")]
        vergeben = set()

        def ersetzt(r):
            """Die endgültige Rechnung zu einer vorläufigen: gleicher Gegenstand und gleiche Menge (fehlt = 1), Preis nur,
            wenn beide einen haben (der endgültige Brief kann ohne lesbare Rechnung sein), später angekommen; die
            nächste gewinnt, jede nur einmal."""
            best, best_d = None, None
            for j, f in enumerate(final):
                if j in vergeben or f.get("name") != r.get("name") or (f.get("menge") or 1) != (r.get("menge") or 1):
                    continue
                if f.get("preis") is not None and r.get("preis") is not None and f["preis"] != r["preis"]:
                    continue
                a, b = r.get("ablauf"), f.get("ablauf")
                d = 0 if a is None or b is None else b - a
                if d < -600:
                    continue
                if best_d is None or abs(d) < best_d:
                    best, best_d = j, abs(d)
            if best is None:
                return False
            vergeben.add(best)
            return True

        bis = (self.letzter["zeit"] if self.letzter and self.letzter["zeit"] else
               max((r.get("zeit") or 0 for r in post), default=0))
        brutto = gebuehr = 0
        for r in post:
            if r.get("art") == "verkauft" and r.get("vorlaeufig") and ersetzt(r):
                continue   # vorläufige Rechnung, die endgültige ist schon da
            if r.get("art") == "verkauft" and r.get("preis"):
                brutto += r["preis"]                       # Gebühr über alle Verkäufe, auch ohne bekannte Item-ID
                gebuehr += r.get("gebuehr") or 0
            i = r.get("id") or self.name2id.get(r.get("name"))
            if not i:
                continue
            e, menge = out[int(i)], int(r.get("menge") or 1)
            if r.get("art") == "verkauft":
                e["verkauft"] += menge
                e["n"] += 1
                if (r.get("zeit") or 0) >= bis - ABSATZ_STUNDEN * 3600:
                    e["verkauft_72h"] += menge
                if r.get("preis"):
                    e["erloes"] += r["preis"]
            elif r.get("art") == "abgelaufen":
                e["abgelaufen"] += menge
            elif r.get("art") == "angeboten":
                e["angeboten"] += menge
                if r.get("pfand"):
                    e["pfand"] += r["pfand"]
                    e["pfand_stueck"] += menge
        return dict(out), ((gebuehr / brutto, brutto) if brutto else None)

    def beleg(self, i):
        """Abnahme-Belege als Text und ob es einen gibt: geschätzte Käufe aus mindestens MIN_VERGLEICHE Vergleichen über
        MIN_STUNDEN Stunden, oder eigene Verkäufe."""
        teile, ja = [], False
        a = self.abn.get(i)
        vgl = lambda n: f"{n} Vergleich" + ("e" if n != 1 else "")
        if a and a[0] > 0:
            teile.append(f"geschätzt {a[0]} Stück in {a[2]:.1f} h gekauft ({vgl(a[3])})")
            if a[3] >= MIN_VERGLEICHE and a[2] >= MIN_STUNDEN:
                ja = True
            else:
                teile[-1] += ", zu wenig für einen Beleg"
        elif a:
            teile.append(f"in {a[2]:.1f} h kein Kauf geschätzt ({vgl(a[3])})")
        # Langzeit: nur Anzeige, wenn es Vergleiche vor den letzten 7 Tagen gibt; Beleg und Menge bleiben bei 7 Tagen
        a30 = self.abn30.get(i)
        if a30 and a30[3] > (a[3] if a else 0):
            teile.append(f"{LANGZEIT_TAGE} Tage: geschätzt {a30[0]} Stück in {a30[2]:.1f} h gekauft ({vgl(a30[3])})")
        e = self.eigen.get(i)
        if e and e["verkauft"]:
            quote = e["verkauft"] / (e["verkauft"] + e["abgelaufen"]) if e["abgelaufen"] else 1
            teile.append(f"eigene Verkäufe {e['verkauft']} Stück ({prozent(quote)} verkauft)")
            ja = True
        elif e and e["abgelaufen"]:
            teile.append(f"eigene Angebote: {e['abgelaufen']} Stück abgelaufen")
        return "; ".join(teile) if teile else "keine Abnahme-Belege", ja

    def absatz(self, i):
        """Wie viel Stück mit Beleg abgehen: geschätzte Käufe in den beobachteten Stunden (nie hochgerechnet, bei mehr
        als ABSATZ_STUNDEN Stunden auf diese umgelegt), mindestens die eigenen Verkäufe der letzten ABSATZ_STUNDEN."""
        menge = 0
        a = self.abn.get(i)
        if a and a[0] > 0 and a[3] >= MIN_VERGLEICHE and a[2] >= MIN_STUNDEN:
            menge = int(a[0] * min(1.0, ABSATZ_STUNDEN / a[2]))
        e = self.eigen.get(i)
        return max(menge, e["verkauft_72h"] if e else 0)


# --- Empfehlungen --------------------------------------------------------------------------------------------------------
def naechstes(stufen, menge):
    """Preis des ersten Stücks, das nach dem Kauf der billigsten «menge» Stück übrig bleibt (None: unbekannt oder keins)."""
    rest = menge
    for u, n in stufen:
        if n > rest:
            return u
        rest -= n
    return None


def handel(m):
    """Kaufen und wieder verkaufen: Angebote unter (Tiefstpreis 7 Tage × 0,95) / (1 + Marge). Wieder einstellen zum
    Tiefstpreis der 7 Tage, ausser das nächste Angebot danach ist billiger: dann 1c darunter."""
    mit, ohne = [], []
    for i, p in m.jetzt.items():
        if not p.get("stufen"):
            continue
        _, _, belastbar = m.verkauf(i)
        if not belastbar:
            continue
        ziel = m.kz[i]["boden7"]
        grenze = ziel * (1 - GEBUEHR) / (1 + m.marge)
        im_angebot = sum(n for u, n in p["stufen"] if u <= grenze)
        if not im_angebot:
            continue
        text, ja = m.beleg(i)
        cap = m.absatz(i) if ja else im_angebot
        n_kauf, k_kauf = 0, 0
        for u, n in p["stufen"]:
            if u > grenze or n_kauf >= cap:
                break
            t = min(n, cap - n_kauf)
            n_kauf += t
            k_kauf += u * t
        if not n_kauf:
            continue
        nxt = naechstes(p["stufen"], n_kauf)
        if nxt is None and p["menge"] > sum(n for _, n in p["stufen"]):
            nxt = p["stufen"][-1][0] + 1   # Preisstufen abgeschnitten: der Rest kostet mindestens die letzte bekannte
        um = min(ziel, nxt - 1) if nxt else ziel
        gewinn = n_kauf * um * (1 - GEBUEHR) - k_kauf
        e = {"id": i, "name": m.name(i), "grenze": grenze, "ziel": ziel, "um": um, "naechstes": nxt, "kz": m.kz[i],
             "beleg": text, "im_angebot": im_angebot, "menge": n_kauf, "kosten": k_kauf, "gewinn": gewinn,
             "marge": gewinn / k_kauf if k_kauf else None}
        if ja and cap > 0 and e["marge"] is not None and e["marge"] >= m.marge:
            mit.append(e)
        else:
            e["grund"] = ("keine Abnahme-Belege" if not ja else
                          f"nächstes Angebot {geld(nxt)} liegt zu tief" if nxt and nxt - 1 < ziel else "Marge zu klein")
            ohne.append(e)
    mit.sort(key=lambda e: -e["gewinn"])
    ohne.sort(key=lambda e: -e["gewinn"])
    return mit, ohne


def trend_text(k):
    """Warnungen zum Preis: fällt in den letzten 3 Tagen; liegt deutlich über dem Wert der 30 Tage."""
    if not k:
        return ""
    s = ""
    t = k.get("trend")
    if t is not None and t <= -0.10:
        s += f" Achtung: Tiefstpreis fällt ({prozent(t)} in den letzten 3 Tagen)."
    b7, b30 = k.get("boden7"), k.get("boden30")
    if b7 and b30 and k.get("n30", 0) > k.get("n7", 0) and b7 >= b30 * (1 + LANGZEIT_WARNUNG):
        s += (f" Achtung: Tiefstpreis 7 Tage {geld(round(b7))} liegt {prozent(b7 / b30 - 1)} über dem Wert der "
              f"{LANGZEIT_TAGE} Tage ({geld(round(b30))}).")
    return s


def langzeit_text(k):
    """Median der Tiefstpreise der letzten 30 Tage, nur wenn es Scans vor den letzten 7 Tagen gibt."""
    if not k or k.get("boden30") is None or k.get("n30", 0) <= k.get("n7", 0):
        return "–"
    return f"{geld(round(k['boden30']))} ({k['n30']} Scans, {k['tage30']} Tage)"


def mit_warnung(k):
    """Warnungen als Fortsetzung eines Belegs in einer Tabellenzelle (mit Punkt davor)."""
    w = trend_text(k)
    return "." + w if w else ""


def dauer(stunden):
    return f"{round(stunden * 60)} Min" if stunden < 1 else f"{stunden:.1f} h"


def bestand(m, mit_gebunden=False):
    """Charakter (ohne Realm) -> {Item-ID: Anzahl} aus Taschen und Bank; dazu die Kontobank. Gebundene Stücke nur mit
    mit_gebunden (zum Herstellen ja, zum Verkaufen nein)."""
    felder = ("liste", "gebunden") if mit_gebunden else ("liste",)
    out = {}
    for key, c in als_dict(m.db.get("chars")).items():
        if not isinstance(c, dict):
            continue
        name = str(key).split("-")[0]
        b = defaultdict(int)
        for teil in ("taschen", "bank"):
            for feld in felder:
                for i, n in liste((c.get(teil) or {}).get(feld)).items():
                    b[i] += n
        out[name] = dict(b)
    konto = defaultdict(int)
    for feld in felder:
        for i, n in liste((m.db.get("kontobank") or {}).get(feld)).items():
            konto[i] += n
    return out, dict(konto)


def herstellen(m):
    """Pro Charakter und Beruf jedes gelernte Rezept mit Ergebnis: Wert, Kosten, Marge, wie oft aus dem Bestand."""
    inv, konto = bestand(m, mit_gebunden=True)
    out = []
    rezeptnamen = als_dict(m.db.get("rezeptNamen"))
    for key, c in als_dict(m.db.get("chars")).items():
        if not isinstance(c, dict):
            continue
        char = str(key).split("-")[0]
        mein = defaultdict(int, inv.get(char, {}))
        for i, n in konto.items():
            mein[i] += n
        for beruf, b in als_dict(c.get("rezepte")).items():
            if not isinstance(b, dict):
                continue
            for r in rezepte(b.get("liste")):
                if not r["out"]:
                    continue
                menge = (r["qmin"] + r["qmax"]) / 2
                v, herkunft, belastbar = m.verkauf(r["out"])
                wert = v * menge * (1 - GEBUEHR) if v is not None else None
                if wert is None:
                    s = (m.info.get(r["out"]) or {}).get("s")
                    if s:
                        wert, herkunft, belastbar = s * menge, "Händler-Ankauf", True
                reag = [(i, n) for i, n in r["reag"] if n > 0]
                kosten, fehlt = 0, []
                for i, n in reag:
                    k, wo = m.einkauf(i, n)
                    if k is None:
                        fehlt.append(m.name(i))
                    else:
                        kosten += k
                aus_bestand = min((mein.get(i, 0) // n for i, n in reag), default=0)
                rname = rezeptnamen.get(r["id"]) or rezeptnamen.get(str(r["id"])) or m.name(r["out"])
                e = {"char": char, "beruf": beruf, "id": r["id"], "rezept": rname, "out": r["out"], "menge": menge,
                     "wert": wert, "herkunft": herkunft, "belastbar": belastbar, "kosten": None if fehlt else kosten,
                     "fehlt": fehlt, "farbe": FARBE.get(r["farbe"], "?"), "aus_bestand": aus_bestand}
                if wert is not None and not fehlt:
                    e["gewinn"] = wert - kosten
                    e["marge"] = (wert - kosten) / kosten if kosten else None
                e["beleg"], e["absatz"] = m.beleg(r["out"])
                out.append(e)
    out.sort(key=lambda e: -(e.get("gewinn") or -1e12))
    return out


def plan_material(plan):
    """Item-IDs, die der Berufe-Plan als Material braucht (data/kombi/bedarf_lw_vz.csv, Spalte «material»)."""
    namen = {r["material"] for r in at._read(os.path.join(at.D, "kombi", "bedarf_lw_vz.csv")) if r.get("material")}
    return {i for i, e in plan.items() if e["material"] in namen}


def verkaufen(m):
    """Was im Bestand im AH mehr bringt als beim Händler (gebundene Teile ausgenommen)."""
    inv, konto = bestand(m)
    plan = plan_material(m.plan)
    orte = defaultdict(list)
    menge = defaultdict(int)
    for char, b in inv.items():
        for i, n in b.items():
            orte[i].append(f"{char} {n}")
            menge[i] += n
    for i, n in konto.items():
        orte[i].append(f"Kontobank {n}")
        menge[i] += n
    out, haendler = [], []
    for i, n in menge.items():
        info = m.info.get(i) or {}
        if info.get("b") == 1:
            continue   # beim Aufheben gebunden: nicht handelbar
        netto = m.netto(i)
        ankauf = info.get("s") or 0
        _, herkunft, belastbar = m.verkauf(i)
        if netto is not None and netto > ankauf * 1.1:
            text, ja = m.beleg(i)
            # empfohlen höchstens so viel, wie mit Beleg abgeht; der Rest drückt sonst den eigenen Preis
            empf = min(n, m.absatz(i)) if ja else 0
            out.append({"id": i, "name": m.name(i), "menge": n, "empfohlen": empf, "netto": netto, "summe": netto * n,
                        "summe_empf": netto * empf, "herkunft": herkunft, "belastbar": belastbar, "beleg": text,
                        "absatz": ja and empf > 0, "orte": ", ".join(orte[i]), "plan": i in plan})
        elif ankauf and (netto is None or netto <= ankauf * 1.1) and info.get("q") == 0:
            haendler.append({"id": i, "name": m.name(i), "menge": n, "summe": ankauf * n})
    out.sort(key=lambda e: -e["summe"])
    haendler.sort(key=lambda e: -e["summe"])
    return out, haendler


ZEILE = re.compile(r"^(\d\d)\.(\d\d)\. (\d\d):(\d\d):(\d\d) \| (ANGELN|SAMMELN|BEUTE) \| (.*)$")
GELD_ZEILE = re.compile(r"^(\d\d)\.(\d\d)\. (\d\d):(\d\d):(\d\d) \| GELD \| (.*)$")
SONST = re.compile(r"(?:^| \| )sonst \+([\dgsc ]+?)(?: \||$)")
POSTEN = re.compile(r"(\d+)x ([^,|]+?) \((\d+)\)")
GELD = re.compile(r"Geld \+([\dgsc ]+)")
MUENZ_RAND = 60     # Sekunden vor und nach einem Durchgang, in denen Geld «sonst» noch zur Beute zählt


def farmen(m):
    """Wert pro Stunde je Tätigkeit und Gebiet aus ANGELN, SAMMELN und BEUTE (Durchgänge mit Pausen unter 10 Min).
    Geld, das das Testlog keinem Beutefenster zuordnen konnte (GELD «sonst»), zählt zu einem Durchgang «Gegner» im
    selben Gebiet, wenn es währenddessen kam (am 15.10. so bei schnellem Plündern beobachtet)."""
    jahr = int(m.letzter["datum"][:4]) if m.letzter else datetime.now().year
    ereignisse = defaultdict(list)
    muenzen = defaultdict(list)
    for zeile in m.db.get("log") or []:
        zg = GELD_ZEILE.match(str(zeile))
        if zg:
            felder = zg.group(6).split(" | ")
            s = SONST.search(zg.group(6))
            if s and len(felder) >= 2:
                try:
                    k = at.kupfer(s.group(1))
                except ValueError:
                    continue
                t = datetime(jahr, int(zg.group(2)), int(zg.group(1)), int(zg.group(3)), int(zg.group(4)), int(zg.group(5)))
                muenzen[felder[1].split(" > ")[0]].append([t, k, False])
            continue
        z = ZEILE.match(str(zeile))
        if not z:
            continue
        t = datetime(jahr, int(z.group(2)), int(z.group(1)), int(z.group(3)), int(z.group(4)), int(z.group(5)))
        felder = z.group(7).split(" | ")
        if len(felder) < 5:
            continue
        gebiet = felder[1].split(" > ")[0]
        rest = " | ".join(felder[4:])
        art = {"ANGELN": "Angeln",
               "BEUTE": "Gegner" if felder[4].startswith("Kreatur") else "Beute"}.get(z.group(6))
        if not art:
            art = felder[4] if not felder[4].startswith(("Kreatur", "Objekt", "Gegenstand")) else "Sammeln"
        wert, ohne = 0.0, []
        for n, name, i in POSTEN.findall(rest):
            i, n = int(i), int(n)
            _, _, belastbar = m.verkauf(i)
            # AH-Preis nur mit Verlauf (sonst Händler-Ankauf), gebundene Beute nur zum Händler
            netto = m.netto(i) if belastbar and (m.info.get(i) or {}).get("b") != 1 else None
            if netto is None and i not in m.info:
                ohne.append(name.strip())   # kein Preis bekannt (Gegenstands-Infos erst ab Testlog 3.6)
            ankauf = (m.info.get(i) or {}).get("s") or 0
            wert += n * max(netto or 0, ankauf)
        g = GELD.search(rest)
        if g:
            try:
                wert += at.kupfer(g.group(1))
            except ValueError:
                pass
        ereignisse[(art, gebiet)].append((t, wert, ohne))
    out = []
    for (art, gebiet), ev in ereignisse.items():
        ev.sort(key=lambda x: x[0])
        laeufe, lauf = [], [ev[0]]
        for e in ev[1:]:
            if (e[0] - lauf[-1][0]).total_seconds() > BOUT_PAUSE:
                laeufe.append(lauf)
                lauf = [e]
            else:
                lauf.append(e)
        laeufe.append(lauf)
        sek, wert, n, anzahl, ohne, sonst = 0.0, 0.0, 0, 0, set(), 0
        for l in laeufe:
            if len(l) < MIN_EREIGNISSE:
                continue
            abst = [(b[0] - a[0]).total_seconds() for a, b in zip(l, l[1:])]
            sek += (l[-1][0] - l[0][0]).total_seconds() + max(30.0, statistics.median(abst))
            wert += sum(x[1] for x in l)
            if art == "Gegner":
                von, bis = l[0][0] - timedelta(seconds=MUENZ_RAND), l[-1][0] + timedelta(seconds=MUENZ_RAND)
                for mz in muenzen.get(gebiet, []):
                    if not mz[2] and von <= mz[0] <= bis:
                        mz[2] = True
                        sonst += mz[1]
            anzahl += len(l)
            for x in l:
                ohne.update(x[2])
            n += 1
        wert += sonst
        if n and sek > 0:
            out.append({"art": art, "gebiet": gebiet, "laeufe": n, "stunden": sek / 3600, "wert": wert,
                        "pro_stunde": wert / (sek / 3600), "ereignisse": anzahl, "ohne_preis": sorted(ohne),
                        "geld_sonst": sonst})
    out.sort(key=lambda e: -e["pro_stunde"])
    return out


# --- Händler: herstellen für den Händler, Angebote unter dem Händlerpreis -----------------------------------------------
def _plus(*teile):
    """Mehrere {Item-ID: Stück} zusammenzählen (Angebotsbuch)."""
    out = defaultdict(int)
    for t in teile:
        for k, v in (t or {}).items():
            out[k] += v
    return out


UNSICHER = ("AH, nur", "Tiefstpreis 7 Tage", "AH-Tiefstpreis")   # Herkunft ohne bekannte Angebotstiefe: Menge unbekannt


HAENDLER_MAX = 200   # Herstellungen pro Rezept höchstens gerechnet (Taschenplatz, Zeit, Risiko beim Händlerpreis; Wahl von Claude)


def fuer_haendler(m, n_max=HAENDLER_MAX):
    """Gelernte Rezepte, deren Ergebnis der Händler höher bezahlt, als das Material im letzten Scan kostet. Alle Tipps teilen
    ein Angebotsbuch: Herstellung um Herstellung geht an das Rezept mit dem grössten Gewinn, solange er mindestens
    HAENDLER_MIN_STK beträgt, und was ein Rezept kauft, fehlt dem nächsten (Prüfbericht 16.10., A3). Zwischenprodukte, die
    der Charakter selbst herstellen kann (z. B. Geschmeidiger leichter Balg aus Leichtem Balg und Salz), und Geringe
    Essenzen aus geteilten Grossen nimmt es, wenn das billiger ist. Dazu pro Rezept Farbe (gibt es noch Punkte?) und der
    Grenzpreis des teuersten Reagenz für die erste Herstellung."""
    rezeptnamen = als_dict(m.db.get("rezeptNamen"))
    kand = []
    for key, c in als_dict(m.db.get("chars")).items():
        if not isinstance(c, dict):
            continue
        char = str(key).split("-")[0]
        alle = [(beruf, b, r) for beruf, b in als_dict(c.get("rezepte")).items() if isinstance(b, dict)
                for r in rezepte(b.get("liste"))]
        macht = {}
        for _, _, r in alle:
            if r["out"] and r["qmin"] >= 1 and r["reag"]:
                macht.setdefault(r["out"], r)
        for beruf, b, r in alle:
            v = m.ankauf.get(r["out"]) if r["out"] else None
            reag = [(i, n) for i, n in r["reag"] if n > 0]
            if not v or not reag:
                continue
            kand.append({"char": char, "beruf": beruf, "stufe": b.get("stufe"), "r": r, "reag": reag, "macht": macht,
                         "wert": v * (r["qmin"] + r["qmax"]) / 2, "n": 0, "kosten": 0, "geschaetzt": False, "wege": set(),
                         "rezept": rezeptnamen.get(r["id"]) or rezeptnamen.get(str(r["id"])) or m.name(r["out"])})
    buch = defaultdict(int)

    def eine(k):
        """Kosten einer weiteren Herstellung mit dem jetzigen Angebotsbuch: (Kupfer, {Item: Stück}, Wege, geschätzt) oder None."""
        tot, verb, wege, gesch = 0, defaultdict(int), set(), False
        for i, n in k["reag"]:
            kk, wo, v = m.einkauf_ex(i, n, _plus(buch, verb))
            ok = kk is not None and not wo.startswith(UNSICHER)
            z = k["macht"].get(i)
            if z and z is not k["r"]:
                zn = math.ceil(n / max(1, z["qmin"]))
                tz, vz_, okz = 0, defaultdict(int), True
                for j, q in z["reag"]:
                    if q <= 0:
                        continue
                    kj, woj, vj = m.einkauf_ex(j, q * zn, _plus(buch, verb, vz_))
                    if kj is None or woj.startswith(UNSICHER):
                        okz = False
                        break
                    tz += kj
                    for x, y in vj.items():
                        vz_[x] += y
                if okz and (not ok or tz < kk):
                    kk, wo, v, ok = tz, "selbst hergestellt", dict(vz_), True
                    wege.add(f"{m.name(i)} selbst herstellen")
            if not ok:
                return None
            for x in v:
                if not isinstance(x, tuple) and x != i and ESSENZEN.get(i) == x:
                    wege.add(f"{m.name(x)} kaufen und teilen")
            gesch = gesch or "geschätzt" in wo
            tot += kk
            for x, y in v.items():
                verb[x] += y
        return tot, verb, wege, gesch

    offen = list(kand)
    while offen:
        best, weiter = None, []
        for k in offen:
            if k["n"] >= n_max:
                continue
            e = eine(k)
            if not e or k["wert"] - e[0] < HAENDLER_MIN_STK:
                continue          # Preise steigen nur: dieses Rezept lohnt sich nicht mehr
            weiter.append(k)
            if best is None or k["wert"] - e[0] > best[0]:
                best = (k["wert"] - e[0], k, e)
        offen = weiter
        if not best:
            break
        _, k, (tot, verb, wege, gesch) = best
        for x, y in verb.items():
            buch[x] += y
        k["n"] += 1
        k["kosten"] += tot
        k["wege"] |= wege
        k["geschaetzt"] = k["geschaetzt"] or gesch
    out = []
    for k in kand:
        if not k["n"]:
            continue
        einzel = [(i, n, m.einkauf(i, n)[0] or 0) for i, n in k["reag"]]
        haupt = max(einzel, key=lambda x: x[2])
        grenz = (k["wert"] - sum(x[2] for x in einzel if x is not haupt)) / haupt[1]
        out.append({"char": k["char"], "beruf": k["beruf"], "stufe": k["stufe"], "id": k["r"]["id"], "out": k["r"]["out"],
                    "rezept": k["rezept"], "farbe": FARBE.get(k["r"]["farbe"], "?"), "n": k["n"], "kosten": k["kosten"],
                    "wert_je": k["wert"], "gewinn": k["wert"] * k["n"] - k["kosten"], "haupt": m.name(haupt[0]), "grenz": grenz,
                    "geschaetzt": k["geschaetzt"], "wege": sorted(k["wege"])})
    out.sort(key=lambda e: -e["gewinn"])
    return out


def unter_haendler(m):
    """Angebote im letzten Scan unter dem Händlerpreis: kaufen und beim Händler verkaufen (keine AH-Gebühr)."""
    out = []
    for i, p in m.jetzt.items():
        v = p.get("haendler") if p.get("haendler") is not None else m.ankauf.get(i)
        if not v:
            continue
        if p.get("unter") is not None:                      # Testlog 3.7 zählt alle Angebote unter dem Händlerpreis
            n, k = p["unter"], p["unter_kosten"]
        elif p.get("stufen"):
            n = sum(c for u, c in p["stufen"] if u < v)
            k = sum(u * c for u, c in p["stufen"] if u < v)
        elif p["tiefst"] < v:
            n, k = None, p["tiefst"]                         # mindestens ein Angebot, Menge unbekannt
        else:
            continue
        if n == 0:
            continue
        out.append({"id": i, "name": m.name(i), "haendler": v, "n": n, "kosten": k,
                    "gewinn": (v * n - k) if n else (v - k)})
    out.sort(key=lambda e: -e["gewinn"])
    return out


# --- Lage und nächster Schritt pro Charakter -----------------------------------------------------------------------------
def _route():
    """Berufe-Plan (tools/plan_berufe.py): LW-Abschnitte der gewählten Variante, VZ-Möglichkeiten mit und ohne Zauberstäbe."""
    import plan_berufe as pb
    return pb


def _mengen_text(m, bedarf, mein):
    """[(Item-ID, Stück)] -> (Text «braucht», Text «kaufen», Kosten, alles da?)."""
    braucht, kaufen, summe, fehlt_preis = [], [], 0, False
    for i, n in bedarf:
        hast = mein.get(i, 0)
        braucht.append(f"{n} {m.name(i)}" + (f" (hast {hast})" if hast else ""))
        if n > hast:
            k, wo = m.einkauf(i, n - hast)
            if k is None:
                fehlt_preis = True
                kaufen.append(f"{n - hast} {m.name(i)} (kein Preis)")
            else:
                summe += k
                kaufen.append(f"{n - hast} {m.name(i)} ({'Händler' if wo == 'Händler' else 'AH'} {geld(round(k))})")
    return ", ".join(braucht), ", ".join(kaufen), summe, fehlt_preis


def lage(m):
    """Pro Charakter (Schlüssel «Name-Realm» wie im Testlog): kurze Zeilen für /tl tipp. Nur Berufe aus dem Plan."""
    pb = _route()
    lehrer = at._read(LEHRER_CSV) if os.path.exists(LEHRER_CSV) else []
    de = {r["rezept_en"]: r for r in at._read(os.path.join(at.D, "kombi", "rezepte_de.csv"))}
    en_id = {n: int(r["item_id"]) for n, r in pb.IT.items() if (r.get("item_id") or "").isdigit()}
    inv, konto = bestand(m, mit_gebunden=True)
    rezeptnamen = als_dict(m.db.get("rezeptNamen"))
    lw_segs = pb.segments(pb.wp[pb.CHOICE])
    seg_by_erg = {sg[5]: sg for sg in lw_segs if sg[5]}
    # Wie lange der Plan ein Material braucht, auch über Zwischenprodukte (Salz -> Geschmeidiger Balg -> Lederhose)
    letzte = {}
    for _ in range(4):
        for von, bis, rez, n, mats, erg, _q in lw_segs:
            for mt in mats:
                letzte[("LW", mt)] = max(letzte.get(("LW", mt), 0), bis, letzte.get(("LW", erg), 0) if erg else 0)
    for (a, b_), opts in pb.vz_options().items():
        for o in opts:
            for mt in o["mats"]:
                letzte[("VZ", mt)] = max(letzte.get(("VZ", mt), 0), b_)
    out = {}
    for key, c in als_dict(m.db.get("chars")).items():
        if not isinstance(c, dict):
            continue
        char = str(key).split("-")[0]
        mein = defaultdict(int, inv.get(char, {}))
        for i, n in konto.items():
            mein[i] += n
        zeilen = []
        for beruf, b in als_dict(c.get("rezepte")).items():
            kurz = BERUF_KURZ.get(beruf)
            if not kurz or not isinstance(b, dict) or not str(b.get("stufe") or "").isdigit():
                continue
            stufe = int(b["stufe"])
            gelernt = rezepte(b.get("liste"))
            namen = {str(rezeptnamen.get(r["id"]) or rezeptnamen.get(str(r["id"])) or ""): r for r in gelernt}
            by_out = {r["out"]: r for r in gelernt if r["out"]}
            if stufe >= 150:
                zeilen.append(f"{kurz} {stufe}: Ziel des Plans erreicht.")
                continue
            if kurz == "LW":
                seg = next((sg for sg in lw_segs if sg[0] <= stufe < sg[1]), None)
                if not seg:
                    continue
                von, bis, rez, n, mats, _, _ = seg
                rest = max(1, math.ceil(n * (bis - stufe) / (bis - von)))
                item = en_id.get(rez)
                g = by_out.get(item)
                name = (de.get(rez) or {}).get("deutsch") or rez
                lern = ""
                if not g:
                    lr = next((x for x in lehrer if x["item_id"] and item and int(x["item_id"]) == item), None)
                    lern = (f" Erst lernen bei {lr['lehrer']} (ab {kurz} {lr['ab_fertigkeit']}, {lr['kosten']})." if lr
                            else " Rezept noch nicht gelernt.")
                bedarf = [(en_id[mt], math.ceil(je * rest)) for mt, je in mats.items() if mt in en_id]
                # Zwischenprodukte (z. B. Geschmeidiger leichter Balg): selbst herstellen, wenn das Rezept da ist und es
                # billiger ist als im AH; dann kommen dessen Materialien auf die Liste
                selbst = []
                for mt, je in mats.items():
                    zw = seg_by_erg.get(mt)
                    i = en_id.get(mt)
                    if not zw or not i or i not in by_out:
                        continue
                    fehlt_n = max(0, math.ceil(je * rest) - mein.get(i, 0))
                    if not fehlt_n:
                        continue
                    k_ah = m.einkauf(i, fehlt_n)[0]
                    teile = [(en_id[x], math.ceil(q * fehlt_n)) for x, q in zw[4].items() if x in en_id]
                    k_selbst = sum((m.einkauf(j, max(0, n_ - mein.get(j, 0)))[0] or 0) if n_ > mein.get(j, 0) else 0
                                   for j, n_ in teile)
                    if k_ah is None or k_selbst < k_ah:
                        bedarf = [(j, n_ - (fehlt_n if j == i else 0)) for j, n_ in bedarf] + teile
                        rz = by_out[i]
                        selbst.append(f"{fehlt_n}× {m.name(i)} selbst herstellen ({FARBE.get(rz['farbe'], '?')}; "
                                      f"{geld(round(k_selbst))} statt {geld(round(k_ah)) if k_ah is not None else 'kein Angebot'} im AH)")
                zusammen = defaultdict(int)
                for j, n_ in bedarf:
                    zusammen[j] += n_
                bedarf = [(j, n_) for j, n_ in zusammen.items() if n_ > 0]
                braucht, kaufen, summe, _ = _mengen_text(m, bedarf, mein)
                farbe = f", {FARBE.get(g['farbe'], '?')}" if g else ""
                t = f"{kurz} {stufe}: weiter bis {bis:.0f} mit etwa {rest}× {name}{farbe}.{lern} Braucht {braucht}."
                if selbst:
                    t += " Vorher " + "; ".join(selbst) + "."
                if kaufen:
                    t += f" Kaufen: {kaufen} = {geld(round(summe))}."
                v = m.ankauf.get(item) if item else None
                if v and rez in pb.VERKAUFEN:
                    t += f" Danach beim Händler verkaufen: {geld(v)} je Stück."
                zeilen.append(t)
            else:
                rng = next(((a, b_) for (a, b_) in pb.vz_options() if a <= stufe < b_), None)
                if not rng:
                    continue
                kands = []
                for staebe in (False, True):
                    for o in pb.vz_options(staebe)[rng]:
                        if staebe and "Zauberstab" not in o["routes"]:
                            continue
                        lo, hi = o.get("nur", rng)
                        if not (lo <= stufe < hi):
                            continue
                        de_name = (de.get(o["rezept"]) or {}).get("deutsch") or o["rezept"]
                        kann = de_name in namen
                        lr = next((x for x in lehrer if x["eintrag"] == de_name), None)
                        ab = int(lr["ab_fertigkeit"]) if lr and lr["ab_fertigkeit"] else int(pb.learn_at(o["rezept"]) or 0)
                        if not kann and ab > stufe:
                            continue
                        pts = rng[1] - rng[0]
                        punkte = min(hi, rng[1]) - stufe
                        anzahl = max(1, math.ceil(o["n"] * punkte / pts))
                        bedarf = [(en_id[mt], math.ceil(je * anzahl)) for mt, je in o["mats"].items() if mt in en_id]
                        braucht, kaufen, summe, fehlt = _mengen_text(m, bedarf, mein)
                        zur = o.get("zurueck", 0.0) * 100 * anzahl
                        lern = "" if de_name in namen else (f" Erst lernen bei {lr['lehrer']} ({lr['kosten']})." if lr else "")
                        kands.append(((summe - zur) / max(1, punkte) if not fehlt else 1e9, de_name, anzahl, braucht, kaufen,
                                      summe, zur, lern, staebe, min(hi, rng[1])))
                if not kands:
                    continue
                kands.sort(key=lambda x: x[0])
                best = next((k for k in kands if not k[8]), kands[0])
                t = (f"{kurz} {stufe}: weiter bis {best[9]:.0f} mit etwa {best[2]}× {best[1]}.{best[7]} Braucht {best[3]}."
                     + (f" Kaufen: {best[4]} = {geld(round(best[5]))}." if best[4] else ""))
                stab = next((k for k in kands if k[8]), None)
                if stab and stab[0] < best[0] - 1:
                    t += (f" Günstiger wäre {stab[1]} (Vorschlag, berufe-plan.md §9): netto etwa {geld(round(stab[0]))} "
                          f"statt {geld(round(best[0]))} je Punkt, der Händler kauft die Stäbe zurück.")
                zeilen.append(t)
        # Überschuss: Material des Plans, das bei der jetzigen Fertigkeit nicht mehr gebraucht wird
        stufen = {BERUF_KURZ.get(bf): int(b["stufe"]) for bf, b in als_dict(c.get("rezepte")).items()
                  if BERUF_KURZ.get(bf) and isinstance(b, dict) and str(b.get("stufe") or "").isdigit()}
        ueber = []
        for mt, i in en_id.items():
            n = mein.get(i, 0)
            if not n:
                continue
            noch = [k for (k, x), bis in letzte.items() if x == mt and (k not in stufen or stufen[k] < bis)]
            if noch or not any(x == mt for (_, x) in letzte):
                continue
            netto = m.netto(i)
            v = m.ankauf.get(i) or 0
            wo = (f"im AH etwa {geld(round(netto))} je Stück nach Gebühr" if netto and netto > v
                  else f"beim Händler {geld(v)} je Stück" if v else "")
            if wo:
                ueber.append(f"{n} {m.name(i)} ({wo})")
        if ueber:
            zeilen.append("Überschuss (braucht dein Plan nicht mehr): " + ", ".join(ueber)
                          + ". Ob es im AH abgeht, zeigt erst die Abnahme aus mehreren Scans.")
        if zeilen:
            out[str(key)] = zeilen
    # Sammler (ohne Lederverarbeitung und Verzauberkunst): auch Charaktere ohne Berufsfenster, aus Protokoll und chars
    stand = (datetime.strptime(m.letzter["datum"], "%Y-%m-%d %H:%M").strftime("%d.%m. %H:%M") if m.letzter else "?")
    for key, z in sammler_zustand(m).items():
        char = key.split("-")[0]
        mein = defaultdict(int, inv.get(char, {})) if char in inv else None
        if mein is not None:
            for i, n in konto.items():
                mein[i] += n
        zs = sammler(m, key, z, mein, stand)
        if zs:
            out.setdefault(key, [])
            out[key] = zs + out[key]
    return out


# --- Sammler und Listen für das Testlog ---------------------------------------------------------------------------------
GELD_SITZUNG = re.compile(r"\| Geld ([\dgsc ]+) \|")
EXTRA_BEOBACHTEN = (7428, 252436, 252437, 2592)   # Markt-Analyse 16.10.: Shadowcat Hide (Händlerpreis in Forever unbekannt),
                                                  # Mystisches und Kraftvolles mittleres Rüstungsset, Wollstoff


def sammler_zustand(m):
    """Charakter («Name-Realm» wie im Testlog) -> Berufe {Name: (Stufe, Maximum)}, Geld (Kupfer), Datum und gesehene Beute
    {Item-ID: Stück}: aus chars (ab Testlog 3.7.1: berufe, geld), sonst aus den Zeilen nach der letzten SITZUNG des
    Charakters (BERUF, GELD «Bestand», Geld in der SITZUNG-Zeile, BEUTE und SAMMELN)."""
    out, wer = {}, None
    for zeile in m.db.get("log") or []:
        zeile = str(zeile)
        teile = zeile.split(" | ")
        if len(teile) < 3:
            continue
        art = teile[1]
        if art == "SITZUNG" and len(teile) >= 7:
            wer = teile[6].strip()
            e = out.setdefault(wer, {"berufe": {}, "geld": None, "datum": None, "beute": defaultdict(int)})
            g = GELD_SITZUNG.search(zeile)
            if g:
                try:
                    e["geld"], e["datum"] = at.kupfer(g.group(1).strip()), teile[0]
                except ValueError:
                    pass
            continue
        if art == "ENDE":
            wer = None
            continue
        if not wer or len(teile) < 7:
            continue
        e = out[wer]
        if art == "BERUF":
            b = re.match(r"^(.*\S) (\d+)/(\d+)$", teile[6].strip())
            if b:
                e["berufe"][b.group(1)] = (int(b.group(2)), int(b.group(3)))
                e["datum"] = teile[0]
        elif art == "GELD":
            g = re.search(r"Bestand ([\dgsc ]+)$", zeile)
            if g:
                try:
                    e["geld"], e["datum"] = at.kupfer(g.group(1).strip()), teile[0]
                except ValueError:
                    pass
        elif art in ("BEUTE", "SAMMELN"):
            for n, _, i in POSTEN.findall(" | ".join(teile[6:])):
                e["beute"][int(i)] += int(n)
    for key, c in als_dict(m.db.get("chars")).items():
        if not isinstance(c, dict):
            continue
        e = out.setdefault(str(key), {"berufe": {}, "geld": None, "datum": None, "beute": defaultdict(int)})
        for name, v in als_dict(c.get("berufe")).items():
            b = re.match(r"^(\d+)/(\d+)$", str(v))
            if b:
                e["berufe"][str(name)] = (int(b.group(1)), int(b.group(2)))
        if isinstance(c.get("geld"), (int, float)):
            e["geld"] = int(c["geld"])
            if c.get("geldZeit"):
                e["datum"] = datetime.fromtimestamp(int(c["geldZeit"])).strftime("%d.%m. %H:%M")
    return out


def ah_statt_haendler(m, ids):
    """[(Item-ID, AH netto je Stück, Händler je Stück, Stück im Angebot)] für Beute, die im AH nach Gebühr mindestens VIELFACH
    mal so viel bringt wie beim Händler (ohne Absatz-Beleg; Preis wie verkauf(): mit Verlauf der kleinere aus jetzt und
    7 Tagen). Ohne gebundene, graue und Plan-Leder."""
    out = []
    for i in ids:
        info = m.info.get(i) or {}
        if info.get("b") == 1 or info.get("q") == 0 or i in PLAN_LEDER:
            continue
        v, _, _ = m.verkauf(i)
        p = m.jetzt.get(i)
        h = m.ankauf.get(i) or info.get("s") or 0
        if v is None or not p or p["menge"] < MIN_ANGEBOT or not h:
            continue
        netto = v * (1 - GEBUEHR)
        if netto >= VIELFACH * h and netto - h >= 10:
            out.append((i, netto, h, p["menge"]))
    out.sort(key=lambda x: -(x[1] - x[2]))
    return out


def sammler(m, key, z, mein, stand):
    """Zeilen für /tl tipp für Sammler: Charakter mit Kürschnerei oder Kräuterkunde, ohne Lederverarbeitung und
    Verzauberkunst (Plan: Wechsel in Orgrimmar, Stufe A)."""
    b = z["berufe"]
    if not ("Kürschnerei" in b or "Kräuterkunde" in b) or "Lederverarbeitung" in b or "Verzauberkunst" in b:
        return []
    wer = ", ".join(f"{n} {b[n][0]}" for n in ("Kürschnerei", "Kräuterkunde") if n in b)
    zeilen = []
    if mein:
        hat = ", ".join(f"{m.name(i)} {mein.get(i, 0)}/{n}" for i, n in STUFE_A.items())
        fehlt = [(i, n - mein.get(i, 0)) for i, n in STUFE_A.items() if n > mein.get(i, 0)]
        kosten = sum((m.einkauf(i, n)[0] or 0) for i, n in fehlt)
        t = f"Sammler ({wer}): bis Orgrimmar Leder behalten, Stufe A braucht {hat}."
        if fehlt and kosten:
            t += f" Was fehlt, kostet im AH etwa {geld(round(kosten))} (Scan {stand})."
    else:
        t = (f"Sammler ({wer}): bis Orgrimmar Leder behalten. Stufe A braucht 99 Fetzen, 62 Leichtes Leder und 27 Leichte Bälge "
             "(dein Bestand ist noch nicht bekannt: erst ab Testlog 3.6 beim Einloggen).")
    zeilen.append(t)
    try:
        pb = _route()
        a = pb.stufen_netto(pb.R["vz"], pb.R["lehrer"], pb.P_SCAN or pb.P)[0]
        gold = f"Gold für den Wechsel in Orgrimmar (Stufe A: Material und Lehrer): etwa {geld(round(a[4] * 100))}"
        if z.get("geld") is not None:
            gold += f"; zuletzt gesehen: {geld(z['geld'])}" + (f" ({z['datum']})" if z.get("datum") else "")
        zeilen.append(gold + ". Reicht es nicht: Beute im AH verkaufen (nächste Zeile) oder Gold schicken lassen.")
    except Exception:
        pass
    ids = set(z.get("beute") or {}) | set(mein or {})
    gut = ah_statt_haendler(m, ids)[:5]
    if gut:
        zeilen.append("AH statt Händler (Scan " + stand + ", ohne Absatz-Beleg): " + ", ".join(
            f"{m.name(i)} {geld(round(n))} nach Gebühr (Händler {geld(h)})" for i, n, h, _ in gut)
            + ". Pfand pro Angebot (gemessen 1s für 1 Groben Faden), darum ganze Stapel einstellen.")
    return zeilen


def testlog_listen(m, zustand):
    """KombiDaten.nichtVerkaufen ({Item-ID: Text}, Warnung beim Händler ab Testlog 3.7.1) und KombiDaten.beobachten
    ({Item-ID: true}, zusätzliche Gegenstände mit Preisstufen und Abnahme im AH-Scan)."""
    stand = datetime.strptime(m.letzter["datum"], "%Y-%m-%d %H:%M").strftime("%d.%m.") if m.letzter else "?"
    warn = {i: f"{m.name(i)} (Leder für den Berufe-Plan)" for i in PLAN_LEDER}
    beute = set()
    for z in zustand.values():
        beute |= set(z.get("beute") or {})
    kandidaten = beute | set(m.info)
    for i, n, h, _ in ah_statt_haendler(m, kandidaten)[:WARN_MAX - len(warn)]:
        warn[i] = f"{m.name(i)} (AH etwa {geld(round(n))} nach Gebühr am {stand}, Händler {geld(h)})"
    beob = set(beute) | set(warn) | set(ESSENZEN) | set(ESSENZEN.values()) | set(EXTRA_BEOBACHTEN)
    return warn, sorted(beob)


# --- Ausgabe -------------------------------------------------------------------------------------------------------------
def tipps(m, hdl, her, verk, haendler, farm, fh=(), uh=()):
    t = []
    scan = datetime.strptime(m.letzter["datum"], "%Y-%m-%d %H:%M").strftime("%d.%m. %H:%M") if m.letzter else "?"
    for e in uh[:2]:
        menge = f"{e['n']}x" if e["n"] else "mindestens 1x"
        t.append(f"Unter Händlerpreis: {menge} {e['name']} im AH für zusammen {geld(round(e['kosten']))}, der Händler zahlt "
                 f"{geld(e['haendler'])} je Stück: etwa {geld(round(e['gewinn']))} Gewinn (Scan {scan}; liegt das Angebot noch?).")
    gute = [e for e in fh if e["gewinn"] >= HAENDLER_MIN_GEWINN and (e["farbe"] in ("orange", "gelb", "grün") or e["gewinn"] >= 100)]
    for e in gute[:3]:
        punkte = ", gibt noch Punkte" if e["farbe"] in ("orange", "gelb", "grün") else ""
        wege = f" ({'; '.join(e['wege'])})" if e.get("wege") else ""
        gesch = ", Menge teils geschätzt" if e.get("geschaetzt") else ""
        if e["n"] >= HAENDLER_MAX:
            wege += f"; gerechnet bis {HAENDLER_MAX} Stück, mehr ginge (Taschenplatz beachten)"
        t.append(f"Für den Händler herstellen ({e['char']}, {e['beruf']} {e['stufe']}): {e['n']}× {e['rezept']} ({e['farbe']}{punkte}). "
                 f"Material für {geld(round(e['kosten']))} (AH und Händler{gesch}){wege}, der Händler zahlt {geld(round(e['wert_je']))} "
                 f"je Stück: etwa {geld(round(e['gewinn']))} Gewinn. Lohnt, solange {e['haupt']} höchstens {geld(math.floor(e['grenz']))} "
                 f"kostet (Scan {scan}).")
    for e in hdl[:3]:
        t.append(f"Kaufen: {e['menge']}x {e['name']} bis {geld(round(e['grenze']))} (zusammen {geld(round(e['kosten']))}), "
                 f"wieder einstellen um {geld(round(e['um']))}: etwa {geld(round(e['gewinn']))} Gewinn ({prozent(e['marge'])}). "
                 f"Beleg: {e['beleg']}.{trend_text(e['kz'])}")
    for e in [e for e in her if e.get("gewinn", 0) > 0 and e["belastbar"] and e["absatz"]
              and e.get("marge") is not None and e["marge"] >= m.marge][:3]:
        bestand_text = f"Material im Bestand für {e['aus_bestand']}" if e["aus_bestand"] else "Material zuerst kaufen"
        t.append(f"Herstellen ({e['char']}, {e['beruf']}): {e['rezept']} bringt je {geld(round(e['gewinn']))} "
                 f"({prozent(e['marge'])}), {bestand_text}. Beleg: {e['beleg']}.")
    for e in sorted([e for e in verk if e["belastbar"] and e["absatz"] and not e["plan"]], key=lambda e: -e["summe_empf"])[:3]:
        rest = f" (von {e['menge']}; mehr ist nicht belegt)" if e["empfohlen"] < e["menge"] else ""
        t.append(f"Verkaufen: {e['empfohlen']}x {e['name']}{rest} ({e['orte']}) im AH um "
                 f"{geld(round(e['netto'] / (1 - GEBUEHR)))}, netto etwa {geld(round(e['summe_empf']))}. "
                 f"Beleg: {e['beleg']}.{trend_text(m.kz.get(e['id']))}")
    if haendler:
        summe = sum(e["summe"] for e in haendler)
        t.append(f"Händler: graue Gegenstände für {geld(round(summe))} verkaufen ({len(haendler)} Sorten).")
    # Farmen nur mit genug Zeit und mit einem Preis für jede Beute (sonst wäre der Wert zu tief)
    belegt = [f for f in farm if f["stunden"] >= MIN_FARM_STUNDEN and not f["ohne_preis"]]
    if belegt:
        f = belegt[0]
        t.append(f"Farmen: {f['art']} ({f['gebiet']}) brachte {geld(round(f['pro_stunde']))} pro Stunde "
                 f"({f['laeufe']} Durchgang{'' if f['laeufe'] == 1 else 'e'}, {dauer(f['stunden'])}).")
    return t[:MAX_TIPPS]


def hinweise(m):
    h = []
    if m.letzter:
        n_voll = sum(1 for s in m.scans if not s["unvollstaendig"])
        h.append(f"Preise: eigene AH-Scans, letzter {m.letzter['datum']}, {n_voll} vollständige in der Datei; "
                 f"Verlauf aus data/preise/ah_eigen.csv.")
    else:
        h.append("Noch kein AH-Scan in der Datei: Preise fehlen. Tipps zum Kaufen, Herstellen und Verkaufen kommen "
                 "nach den ersten Scans (Auktionshaus öffnen, Testlog 3.5 oder neuer).")
    h.append("Abnahme = Schätzung aus dem Vergleich zweier Scans (verschwundene billigste Angebote minus neue); "
             "Mengen nie hochgerechnet.")
    h.append("Preise nach 5 % Gebühr; Pfand geht bei Nichtverkauf verloren.")
    h.append("Kaufen, einstellen und entscheiden tust du selbst; die Tipps sind Rechnungen, keine Gewissheit.")
    return h


def lua_str(s):
    s = str(s).replace("\\", "\\\\").replace('"', '\\"').replace("\r", "").replace("\n", "\\n")
    return '"' + "".join(ch for ch in s if ch >= " " or ch == "\\") + '"'


def kombidaten(ordner, m, t, h, stand, zeit, schritte=None, listen=None):
    os.makedirs(ordner, exist_ok=True)
    lua = ["-- KombiDaten: Empfehlungen von Claude, erzeugt von tools/markt.py. Nur Daten, kein Code.",
           "-- Wird bei jedem Lauf ersetzt. Anzeige im Spiel: /tl tipp (KombiTestlog 3.6; «schritte» ab 3.7).",
           "KombiDaten = {",
           f"    stand = {lua_str(stand)},"]
    if zeit:
        lua.append(f"    zeit = {int(zeit)},")
    if m.markt:
        lua.append(f"    markt = {lua_str(m.markt)},")
    lua += ["    tipps = {"]
    lua += [f"        {lua_str(x)}," for x in t]
    lua += ["    },", "    hinweise = {"]
    lua += [f"        {lua_str(x)}," for x in h]
    lua += ["    },"]
    if schritte:   # pro Charakter («Name-Realm» wie im Testlog); nur in diesem Addon beim Spieler, nie im Repo
        lua.append("    schritte = {")
        for key, zeilen in sorted(schritte.items()):
            lua.append(f"        [{lua_str(key)}] = {{")
            lua += [f"            {lua_str(z)}," for z in zeilen]
            lua.append("        },")
        lua.append("    },")
    if listen:   # ab Testlog 3.7.1: Warnung beim Händler und zusätzlich beobachtete Gegenstände
        warn, beob = listen
        lua.append("    nichtVerkaufen = {")
        lua += [f"        [{i}] = {lua_str(t_)}," for i, t_ in sorted(warn.items())]
        lua.append("    },")
        lua.append("    beobachten = {")
        lua += [f"        [{i}] = true," for i in beob]
        lua.append("    },")
    lua += ["}", ""]
    open(os.path.join(ordner, "Daten.lua"), "w", encoding="utf-8").write("\n".join(lua))
    toc = [f"## Interface: {INTERFACE}", "## Title: KombiDaten",
           "## Notes: Empfehlungen von Claude für /tl tipp (erzeugt von tools/markt.py)",
           f"## Version: {stand}", "", "Daten.lua", ""]
    open(os.path.join(ordner, "KombiDaten.toc"), "w", encoding="utf-8").write("\n".join(toc))


def bericht(pfad, m, t, hdl, ohne, her, verk, haendler, farm, stand, fh=(), uh=(), schritte=None):
    L = ["# Markt-Empfehlungen (erzeugt von `tools/markt.py`)", "",
         f"Stand {stand}, Markt {m.markt or '–'}. Nur für dich: enthält deinen Bestand und deine Verkäufe, liegt in "
         "`build/` und kommt nie ins Repo.", "", "## Quellen", ""]
    if m.letzter:
        L.append(f"- Eigene AH-Scans (Testlog 3.5/3.6): {len(m.scans)} Scans in der Datei, letzter {m.letzter['datum']}; "
                 "früherer Verlauf aus `data/preise/ah_eigen.csv` (`tools/ah_aus_testlog.py`). API: "
                 "`C_AuctionHouse.ReplicateItems`, Forever-UI 1.60.1 (https://github.com/Gethe/wow-ui-source/tree/forever).")
    else:
        L.append("- Keine AH-Scans in der Datei: Preise fehlen, darum nur Rezepte und Bestand.")
    L.append(f"- Abnahme: `data/preise/ah_abnahme.csv` und die Scans der Datei (Testlog 3.6), {len(m.abn_rows)} Vergleiche.")
    n_post = len(m.db.get("ahPost") or [])
    L.append(f"- Eigene Angebote und AH-Briefe (Testlog 3.6): {n_post} Einträge.")
    gb = (f"; in deinen Verkäufen {prozent(m.gebuehr_eigen[0])} von {geld(m.gebuehr_eigen[1])}"
          if m.gebuehr_eigen else "")
    L.append(f"- Gebühr 5 %: AHledger, Seite «Auction House» (https://ahledger.com/wow-forever/auction-house){gb}.")
    L.append("- Händlerpreise (Einkauf): `data/kombi/preise_zusatz.csv`, `data/rechnung/Preise.csv`; Ankauf durch Händler: "
             "Client (`C_Item.GetItemInfo`, Testlog 3.6).")
    L.append("- Rezepte und Bestand: Testlog 3.6 (Berufsfenster, Taschen, Bank, Kontobank).")
    L += ["", "## Kurz (wie /tl tipp)", ""]
    L += [f"{n}. {x}" for n, x in enumerate(t, 1)] or ["Noch keine Empfehlung mit Beleg."]
    L += ["", "## Nächster Schritt pro Charakter (wie /tl tipp)", "",
          "Abschnitt des Berufe-Plans für die jetzige Fertigkeit (`tools/plan_berufe.py`), was fehlt und was es im letzten Scan "
          "kostet, ob das Rezept noch zu lernen ist (`data/kombi/lehrer.csv`), bei Verzauberkunst der Zauberstab-Weg als Vergleich "
          "(Vorschlag, berufe-plan.md §9). Überschuss = Material des Plans, das die Fertigkeit nicht mehr braucht.", ""]
    if schritte:
        for key, zeilen in sorted(schritte.items()):
            L.append(f"**{str(key).split('-')[0]}**")
            L += [f"- {z}" for z in zeilen]
            L.append("")
    else:
        L.append("Keine Berufe des Plans in der Datei (Berufsfenster einmal öffnen, Testlog 3.6).")
    L += ["", "## Für den Händler herstellen", "",
          "Rezepte, deren Ergebnis der Händler höher bezahlt, als das Material im letzten Scan kostet (Händlerpreis aus dem "
          "Forever-Client). Menge: bis die nächste Herstellung mehr kostet, als der Händler zahlt. Keine Gebühr, kein "
          "Absatz-Risiko; gilt, solange die Angebote liegen. «Grenzpreis» = so viel darf das teuerste Material höchstens kosten.", ""]
    if fh:
        L += ["Alle Zeilen teilen ein Angebotsbuch (was eine Zeile kauft, fehlt der nächsten); eine weitere Herstellung zählt ab "
              f"{geld(HAENDLER_MIN_STK)} Gewinn, ein Tipp ab {geld(HAENDLER_MIN_GEWINN)} zusammen (Wahl von Claude).", "",
              "| Charakter | Beruf | Rezept | Farbe | Menge | Material | Händler je Stück | Gewinn | Grenzpreis | Wege |",
              "|---|---|---|---|---|---|---|---|---|---|"]
        for e in fh[:25]:
            L.append(f"| {e['char']} | {e['beruf']} {e['stufe']} | {e['rezept']} | {e['farbe']} | {e['n']} | {geld(round(e['kosten']))}"
                     f"{' (teils geschätzt)' if e.get('geschaetzt') else ''} | {geld(round(e['wert_je']))} | {geld(round(e['gewinn']))} | "
                     f"{e['haupt']} bis {geld(math.floor(e['grenz']))} | {'; '.join(e.get('wege') or []) or '–'} |")
    else:
        L.append("Kein Rezept, bei dem der Händler mehr zahlt, als das Material kostet.")
    L += ["", "## Unter dem Händlerpreis im AH", ""]
    if uh:
        L += ["| Gegenstand | Stück | kosten | Händler zahlt | Gewinn |", "|---|---|---|---|---|"]
        for e in uh[:25]:
            L.append(f"| {e['name']} ({e['id']}) | {e['n'] if e['n'] else 'mind. 1'} | {geld(round(e['kosten']))} | "
                     f"{geld(e['haendler'])} | {geld(round(e['gewinn']))} |")
    else:
        tv = str((m.letzter or {}).get("testlog") or "3.5/3.6")
        if tv.startswith(("3.5", "3.6")):
            L.append(f"Keine Angebote unter dem Händlerpreis gefunden. Der letzte Scan stammt von Testlog {tv}: geprüft sind nur "
                     "Gegenstände mit Preisstufen und bekanntem Händlerpreis; erst ab 3.7 prüft der Scan alle Gegenstände, deren "
                     "Daten der Client hat (ab 3.7.1 fragt er fehlende Daten an).")
        else:
            L.append(f"Keine Angebote unter dem Händlerpreis gefunden (Testlog {tv}: geprüft sind alle Gegenstände, deren Daten der "
                     "Client hatte; ab 3.7.1 fragt der Scan fehlende Daten an, der nächste Scan kennt mehr Händlerpreise).")
    L += ["", "## Kaufen und wieder verkaufen", "",
          f"Angebote des letzten Scans unter (Tiefstpreis 7 Tage × 0,95) / (1 + {m.marge:.2f}). Menge höchstens: was in "
          f"den beobachteten Stunden geschätzt gekauft wurde (nie hochgerechnet, bei mehr als {ABSATZ_STUNDEN} Stunden auf "
          f"{ABSATZ_STUNDEN} umgelegt; Beleg ab {MIN_VERGLEICHE} Vergleichen über {MIN_STUNDEN:.0f} Stunde), mindestens "
          f"deine eigenen Verkäufe der letzten {ABSATZ_STUNDEN} Stunden. Wieder einstellen zum Tiefstpreis der 7 Tage, "
          f"ausser das nächste Angebot nach dem Kauf ist billiger (dann 1c darunter). Nur Gegenstände mit Verlauf "
          f"(mindestens {MIN_SCANS} Scans an {MIN_TAGE} Tagen). Trend = Tiefstpreis der letzten 3 Tage gegen die 4 Tage "
          f"davor. «{LANGZEIT_TAGE} Tage» = Median der Tiefstpreise der letzten {LANGZEIT_TAGE} Tage, nur wenn es ältere "
          f"Scans gibt; Warnung, wenn der 7-Tage-Wert {LANGZEIT_WARNUNG * 100:.0f} % oder mehr darüber liegt (Schwelle: "
          f"Wahl von Claude). Die Abnahme der {LANGZEIT_TAGE} Tage steht im Beleg; Preis und Menge richten sich nach den "
          "7 Tagen.", ""]
    if hdl:
        L += [f"| Gegenstand | kaufen bis | Menge | kostet | einstellen um | Gewinn | Marge | Trend | {LANGZEIT_TAGE} Tage "
              "| Beleg |",
              "|---|---|---|---|---|---|---|---|---|---|"]
        for e in hdl:
            tr = prozent(e["kz"]["trend"]) if e["kz"]["trend"] is not None else "–"
            L.append(f"| {e['name']} ({e['id']}) | {geld(round(e['grenze']))} | {e['menge']} | {geld(round(e['kosten']))} | "
                     f"{geld(round(e['um']))} | {geld(round(e['gewinn']))} | {prozent(e['marge'])} | {tr} | "
                     f"{langzeit_text(e['kz'])} | {e['beleg']}{mit_warnung(e['kz'])} |")
    else:
        L.append("Keine Gelegenheit mit Abnahme-Beleg.")
    if ohne:
        L += ["", "Nicht empfohlen (nur zur Beobachtung):", ""]
        L += [f"- {e['name']} ({e['id']}): {e['im_angebot']} Stück unter {geld(round(e['grenze']))}, "
              f"Marge {prozent(e['marge'])}; {e['grund']}; {e['beleg']}" for e in ohne[:15]]
    L += ["", "## Herstellen", "", "Wert = Verkaufspreis × mittlere Menge × 0,95; Kosten = Reagenzien zum Einkaufspreis. "
          "«kurzer Verlauf» = Preis nur aus dem letzten Scan.", ""]
    if her:
        L += ["| Charakter | Beruf | Rezept | Farbe | Wert | Kosten | Gewinn | Marge | aus Bestand | Preis | Beleg |",
              "|---|---|---|---|---|---|---|---|---|---|---|"]
        for e in her:
            kosten = geld(round(e["kosten"])) if e["kosten"] is not None else "fehlt: " + ", ".join(e["fehlt"])
            L.append(f"| {e['char']} | {e['beruf']} | {e['rezept']} | {e['farbe']} | "
                     f"{geld(round(e['wert'])) if e['wert'] is not None else '–'} | {kosten} | "
                     f"{geld(round(e['gewinn'])) if 'gewinn' in e else '–'} | {prozent(e.get('marge'))} | {e['aus_bestand']} | "
                     f"{e['herkunft'] if e['belastbar'] else 'kurzer Verlauf'} | {e['beleg']} |")
    else:
        L.append("Keine Rezepte in der Datei (Berufsfenster einmal öffnen, Testlog 3.6).")
    gefiltert = [f"{str(k).split('-')[0]}, {b}: {v.get('filter')}" for k, c in als_dict(m.db.get("chars")).items()
                 if isinstance(c, dict) for b, v in als_dict(c.get("rezepte")).items() if isinstance(v, dict) and v.get("filter")]
    if gefiltert:
        L += ["", "Rezeptliste vielleicht unvollständig (bisher nur mit Filter gesehen; einmal ohne Filter öffnen): "
              + "; ".join(gefiltert) + "."]
    L += ["", "## Aus dem Bestand verkaufen", "", "Nur, was im AH nach Gebühr mehr als 10 % über dem Händler-Ankauf "
          "bringt; gebundene Teile fehlen. «empfohlen» = höchstens so viel, wie mit Beleg abgeht (wie beim Kaufen). "
          "«Plan» = Material des Berufe-Plans (vorher mit dem Plan abgleichen).", ""]
    if verk:
        L += [f"| Gegenstand | Menge | empfohlen | wo | netto je Stück | zusammen | Preis | {LANGZEIT_TAGE} Tage | Plan | Beleg |",
              "|---|---|---|---|---|---|---|---|---|---|"]
        for e in verk[:40]:
            kz = m.kz.get(e["id"])
            L.append(f"| {e['name']} ({e['id']}) | {e['menge']} | {e['empfohlen']} | {e['orte']} | {geld(round(e['netto']))} | "
                     f"{geld(round(e['summe']))} | {e['herkunft'] if e['belastbar'] else 'kurzer Verlauf'} | "
                     f"{langzeit_text(kz)} | {'ja' if e['plan'] else ''} | {e['beleg']}{mit_warnung(kz)} |")
    else:
        L.append("Kein Bestand mit AH-Preis in der Datei (Taschen beim Einloggen, Bank beim Öffnen, Testlog 3.6).")
    if haendler:
        L += ["", "Graue Gegenstände für den Händler: " + ", ".join(f"{e['menge']}x {e['name']}" for e in haendler[:20]) + "."]
    L += ["", "## Farmen und Angeln", "", f"Aus ANGELN, SAMMELN und BEUTE im Protokoll: Durchgänge mit Pausen unter "
          f"{BOUT_PAUSE // 60} Minuten und mindestens {MIN_EREIGNISSE} Ereignissen; Wert = AH netto (nur mit Verlauf) oder "
          "Händler-Ankauf, der höhere, dazu Geld. «ohne Preis» = Beute ohne AH-Verlauf und ohne Händlerpreis (Gegenstands-"
          f"Infos schreibt erst Testlog 3.6); der Wert ist dann zu tief. Ein Tipp erst ab {round(MIN_FARM_STUNDEN * 60)} "
          "Minuten und ohne solche Beute (Wahl von Claude). «davon Geld sonst» = Geld, das das Testlog keinem "
          "Beutefenster zuordnen konnte (Zeile GELD «sonst»); es zählt zu «Gegner», wenn es während eines Durchgangs im "
          f"selben Gebiet kam (bis {MUENZ_RAND} s davor oder danach).", ""]
    if farm:
        L += ["| Tätigkeit | Gebiet | pro Stunde | Durchgänge | Dauer | Ereignisse | davon Geld sonst | ohne Preis |",
              "|---|---|---|---|---|---|---|---|"]
        L += [f"| {f['art']} | {f['gebiet']} | {geld(round(f['pro_stunde']))} | {f['laeufe']} | {dauer(f['stunden'])} | "
              f"{f['ereignisse']} | {geld(f['geld_sonst']) if f.get('geld_sonst') else '–'} | "
              f"{', '.join(f['ohne_preis'][:8]) + (' …' if len(f['ohne_preis']) > 8 else '') or '–'} |"
              for f in farm]
    else:
        L.append("Noch keine Durchgänge im Protokoll.")
    L += ["", "## Grenzen", "",
          "- Abnahme ist eine Schätzung: Zwischen zwei Scans zählt nur, was von den billigsten Angeboten fehlt, nicht "
          "ablaufen konnte und nicht durch ein neues Angebot bis zu diesem Preis ersetzt wurde. Zu hoch, wenn jemand "
          "zurückzieht und teurer neu einstellt; zu tief, wenn laufend neue Angebote dazukommen. Darum zählt sie erst ab "
          f"{MIN_VERGLEICHE} Vergleichen und wird nie hochgerechnet.",
          "- Annahme: Käufer nehmen die billigsten Angebote zuerst (Waren). Für Ausrüstung ist die Abnahme ungenau.",
          "- Ein Scan zeigt Angebote, keine Verkäufe. Belege für Verkäufe sind nur deine eigenen (AH-Post).",
          "- Beta-Preise sind kein Massstab für den Start am 04.11.2026; zum Start zählen die Scans des eigenen Realms.",
          "- Eine hohe Marge heisst oft: ein einzelnes billiges Angebot oder ein dünner Markt. Menge und Beleg prüfen.", ""]
    os.makedirs(os.path.dirname(pfad), exist_ok=True)
    open(pfad, "w", encoding="utf-8").write("\n".join(L))


def rechne(text, marge=MARGE, aus=AUS):
    db, scans, namen = lade(text)
    m = Markt(db, scans, namen, marge)
    hdl, ohne = handel(m)
    her = herstellen(m)
    verk, haendler = verkaufen(m)
    farm = farmen(m)
    fh, uh = fuer_haendler(m), unter_haendler(m)
    schritte = lage(m)
    listen = testlog_listen(m, sammler_zustand(m))
    t = tipps(m, hdl, her, verk, haendler, farm, fh, uh)
    h = hinweise(m)
    # Stand = letzter Scan (Datum in der Zeit des Spiels); ohne Scan kein Alter im Spiel
    zeit = m.letzter["zeit"] if m.letzter and m.letzter["zeit"] else None
    if m.letzter:
        stand = datetime.strptime(m.letzter["datum"], "%Y-%m-%d %H:%M").strftime("%d.%m. %H:%M")
    else:
        # ohne Scan: Zeit der letzten Protokollzeile (Zeit des Spiels)
        zeilen = [re.match(r"^(\d\d\.\d\d\. \d\d:\d\d)", str(z)) for z in (db.get("log") or [])]
        stand = ([z.group(1) for z in zeilen if z] or ["ohne Daten"])[-1]
    kombidaten(os.path.join(aus, "KombiDaten"), m, t, h, stand, zeit, schritte, listen)
    bericht(os.path.join(aus, "markt.md"), m, t, hdl, ohne, her, verk, haendler, farm, stand, fh, uh, schritte)
    return {"markt": m, "tipps": t, "handel": hdl, "ohne": ohne, "herstellen": her, "verkaufen": verk,
            "haendler": haendler, "farmen": farm, "fuer_haendler": fh, "unter_haendler": uh, "schritte": schritte,
            "listen": listen}


def main():
    args = sys.argv[1:]
    pos = [a for i, a in enumerate(args) if not a.startswith("--") and (i == 0 or args[i - 1] not in ("--marge", "--aus"))]
    if not pos:
        raise SystemExit(USAGE)
    marge = float(args[args.index("--marge") + 1]) if "--marge" in args else MARGE
    aus = args[args.index("--aus") + 1] if "--aus" in args else AUS
    text = open(pos[0], encoding="utf-8", errors="replace").read()
    r = rechne(text, marge, aus)
    m = r["markt"]
    print(f"Markt {m.markt or '–'}, letzter Scan {m.letzter['datum'] if m.letzter else '–'}: {len(r['tipps'])} Tipps, "
          f"{len(r['handel'])} Käufe mit Beleg, {len(r['herstellen'])} Rezepte, {len(r['verkaufen'])} Posten im Bestand, "
          f"{len(r['farmen'])} Tätigkeiten, {len(r['fuer_haendler'])} Rezepte für den Händler, {len(r['unter_haendler'])} "
          f"Angebote unter dem Händlerpreis, nächster Schritt für {len(r['schritte'])} Charakter(e)")
    print("Bericht:", os.path.relpath(os.path.join(aus, "markt.md"), at.ROOT))
    print("Addon:", os.path.relpath(os.path.join(aus, "KombiDaten"), at.ROOT), "(nach Interface\\AddOns\\KombiDaten kopieren)")


if __name__ == "__main__":
    main()
