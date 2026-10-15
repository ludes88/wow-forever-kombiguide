# Lehrerlisten aus dem Testlog übernehmen (Testlog 3.4: Zeile LEHRER beim Öffnen eines Lehrerfensters).
#
# Aufruf:  python3 tools/lehrer_aus_testlog.py <KombiTestlog.lua> [--trocken]
# Ausgabe: data/kombi/lehrer.csv (eine Zeile pro Lehrer und Eintrag: Lernstufe, Kosten, Ort), ohne Charakternamen
#          und ohne den Status beim Messen (gelernt, gesperrt hängt am Charakter, nicht am Lehrer).
#          Lehrer, die schon in der Tabelle stehen und im neuen Testlog vorkommen, werden ersetzt; die übrigen bleiben.
#          Pro Lehrer zählt die Zeile mit den meisten Einträgen (Filter auf alle drei Arten), ergänzt um Einträge,
#          die nur in einer anderen Zeile stehen.
# Englische Namen (Spalte rezept_en): über die Item-ID (data/kombi/items.csv) oder, bei Verzauberungen, über die
# Zauber-ID aus den Rezepten des Testlogs (KombiTestlogDB.rezeptNamen) und data/kombi/rezepte.csv; sonst leer.
import csv, os, re, sys
from lupa import lua51

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "data", "kombi", "lehrer.csv")
COLS = ["lehrer", "kreatur", "art", "karte", "x", "y", "eintrag", "rang", "item_id", "ab_stufe", "beruf", "ab_fertigkeit",
        "kosten_kupfer", "kosten", "rezept_en", "gemessen", "quelle"]
LINE = re.compile(r"^(?P<datum>\d\d\.\d\d\.) (?P<zeit>[\d:]+) \| LEHRER \| (?P<rest>.*)$")
HEAD = re.compile(r"(?P<name>[^|]+?) \(Kreatur (?P<kreatur>\d+)\) \| (?P<art>[^|]+?) \| Filter (?P<filter>[^|]+?) \| (?P<n>\d+) Eintr(?:ag|äge) \| (?P<eintraege>.*)$")
COORD = re.compile(r"\| (?P<karte>\d+) (?P<x>[\d.]+),(?P<y>[\d.]+) \|")
ENTRY = re.compile(r"^(?P<name>.+?)(?: \(Item (?P<item>\d+)\))?(?P<rang> \(Rang\))? (?P<status>lernbar|gesperrt|gelernt)"
                   r"(?:, ab (?P<req>[^,]+?))?(?:, (?P<kosten>(?:\d+g ?)?(?:\d+s ?)?(?:\d+c)?))?$")


def money(text):
    if not text:
        return ""
    total = 0
    for v, u in re.findall(r"(\d+)([gsc])", text):
        total += int(v) * {"g": 10000, "s": 100, "c": 1}[u]
    return str(total)


def requirement(text):
    """«Stufe 10 und Verzauberkunst 50» -> (10, Verzauberkunst, 50); «Lederverarbeitung 110» -> ('', Lederverarbeitung, 110)."""
    stufe, beruf, fert = "", "", ""
    for part in (text or "").split(" und "):
        m = re.match(r"^Stufe (\d+)$", part.strip())
        if m:
            stufe = m.group(1)
            continue
        m = re.match(r"^(.+?) (\d+)$", part.strip())
        if m:
            beruf, fert = m.group(1), m.group(2)
    return stufe, beruf, fert


def english_names(db):
    items = {}
    with open(os.path.join(ROOT, "data", "kombi", "items.csv"), encoding="utf-8-sig") as f:
        lines = [l for l in f if not l.startswith("#")]
    for r in csv.DictReader(lines, delimiter=";"):
        items[r["item_id"]] = r["name"]
    by_spell = {}
    with open(os.path.join(ROOT, "data", "kombi", "rezepte.csv"), encoding="utf-8-sig") as f:
        for r in csv.DictReader(f, delimiter=";"):
            m = re.search(r"(?:recipes/|Rezeptseite )(\d+)", r["quelle"])
            if m:
                by_spell[m.group(1)] = r["rezept"]
    german_to_en = {}
    names = db.rezeptNamen
    if names:
        for spell, name in names.items():
            en = by_spell.get(str(spell))
            if en:
                german_to_en[str(name)] = en
    return items, german_to_en


def main():
    if len(sys.argv) < 2:
        raise SystemExit("Aufruf: python3 tools/lehrer_aus_testlog.py <KombiTestlog.lua> [--trocken]")
    L = lua51.LuaRuntime(unpack_returned_tuples=True)
    L.execute(open(sys.argv[1], encoding="utf-8").read())
    db = L.globals().KombiTestlogDB
    items, german_to_en = english_names(db)
    best = {}
    for i in range(1, len(db.log) + 1):
        m = LINE.match(str(db.log[i]))
        if not m:
            continue
        rest = m.group("rest")
        h = None
        for part_start in range(len(rest)):
            if rest[part_start] == "|" or part_start == 0:
                h = HEAD.search(rest[part_start:].lstrip("| "))
                if h:
                    break
        if not h:
            continue
        c = COORD.search(" | " + rest)
        key = (h.group("name").strip(), h.group("kreatur"))
        entries = h.group("eintraege").split("; ")
        rec = best.setdefault(key, {"art": h.group("art").strip(), "lines": [], "coord": None, "datum": m.group("datum")})
        rec["lines"].append(entries)
        if c and not rec["coord"]:
            rec["coord"] = (c.group("karte"), c.group("x"), c.group("y"))
    rows = []
    for (name, kreatur), rec in best.items():
        lines = sorted(rec["lines"], key=len, reverse=True)
        seen, merged = set(), []
        for entries in lines:
            for e in entries:
                n = ENTRY.match(e.strip())
                label = (n.group("name"), n.group("item")) if n else e   # gleicher Name, anderes Item (Dunkle Lederstiefel)
                if label in seen:
                    continue
                seen.add(label)
                merged.append(e.strip())
        karte, x, y = rec["coord"] or ("", "", "")
        for e in merged:
            n = ENTRY.match(e)
            if not n:
                print(f"nicht erkannt: {name}: {e}")
                continue
            stufe, beruf, fert = requirement(n.group("req"))
            item = n.group("item") or ""
            en = items.get(item, "") or german_to_en.get(n.group("name"), "")
            rows.append({
                "lehrer": name, "kreatur": kreatur, "art": rec["art"], "karte": karte, "x": x, "y": y,
                "eintrag": n.group("name"), "rang": "ja" if n.group("rang") or "lehrling" in n.group("name").lower()
                or "geselle" in n.group("name").lower() else "", "item_id": item, "ab_stufe": stufe, "beruf": beruf,
                "ab_fertigkeit": fert, "kosten_kupfer": money(n.group("kosten")), "kosten": n.group("kosten") or "",
                "rezept_en": en, "gemessen": "2026-" + rec["datum"][3:5] + "-" + rec["datum"][0:2],
                "quelle": "Testlog LEHRER (" + rec["datum"] + ")",
            })
    # Einträge ohne Lernstufe (der Lehrling): Beruf wie die übrigen Einträge desselben Lehrers
    for r in rows:
        if not r["beruf"]:
            same = [x["beruf"] for x in rows if x["lehrer"] == r["lehrer"] and x["beruf"]]
            r["beruf"] = max(set(same), key=same.count) if same else ""
    old = []
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8-sig") as f:
            old = [r for r in csv.DictReader(f, delimiter=";") if (r["lehrer"], r["kreatur"]) not in best]
    allrows = old + rows
    allrows.sort(key=lambda r: (r["art"], r["beruf"] or "~", r["lehrer"], int(r["ab_fertigkeit"] or 0), r["eintrag"]))
    print(f"{len(best)} Lehrer im Testlog, {len(rows)} Einträge; {len(old)} Einträge anderer Lehrer bleiben")
    for (name, kreatur), rec in sorted(best.items()):
        n = sum(1 for r in rows if r["lehrer"] == name)
        print(f"  {name} (Kreatur {kreatur}, {rec['art']}): {n} Einträge, Ort {'/'.join(rec['coord'] or ('-',))}")
    if "--trocken" in sys.argv:
        return
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS, delimiter=";", lineterminator="\n")
        w.writeheader()
        w.writerows(allrows)
    print("geschrieben:", os.path.relpath(OUT, ROOT))


if __name__ == "__main__":
    main()
