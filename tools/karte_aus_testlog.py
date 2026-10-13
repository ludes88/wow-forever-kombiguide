# Kartenecken aus dem Testlog übernehmen und gegen RXP prüfen.
#
# Aufruf:  python3 tools/karte_aus_testlog.py <Testlog-Text oder KombiTestlog.lua> [RXP-Tag]
# Liest alle Zeilen «KARTE» (Testlog 2), trägt die exakten Kartenecken in data/karten/forever_karten.csv ein
# und vergleicht, falls ein RXP-Tag angegeben ist und vendor/rxpguides ihn hat, RXPs Weltkoordinaten
# (.goto Karte/1,A,B) mit RXPs Kommentar-Koordinaten (--c:Zone,x,y). So zeigt sich pro Karte, ob die
# Kommentare zur Forever-Karte passen (Messung vom 13.10.: Thunder Bluff ja, Mulgore nein).
#
# Achsen (gemessen am 13.10. mit Thunder Bluff 1456 und RXPs Koordinaten für Mooranta):
#   C_Map.GetWorldPosFromMapPos liefert (Welt-X = Nord/Süd, Welt-Y = West/Ost).
#   RXP schreibt .goto Karte/1,A,B mit A = Welt-Y (zu Karten-x) und B = Welt-X (zu Karten-y).
#   Also: a0 = Y(0,0), b0 = X(0,0), a1 = Y(1,1), b1 = X(1,1).
import csv, os, re, statistics, subprocess, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
RXP = os.environ.get("RXP_DIR", os.path.join(ROOT, "vendor", "rxpguides"))
CSV_PATH = os.path.join(ROOT, "data", "karten", "forever_karten.csv")
FIELDS = ["karte", "name", "a0", "b0", "a1", "b1", "quelle", "status"]
USAGE = "Aufruf: python3 tools/karte_aus_testlog.py <Testlog-Text oder KombiTestlog.lua> [RXP-Tag]"
# Eine KARTE-Zeile, als Text aus /tl zeigen oder als Lua-Zeichenkette aus der SavedVariables-Datei
LINE = re.compile(
    r"^\s*\"?(?P<datum>\d\d\.\d\d\.) [\d:]+ \| KARTE \|.*?\| (?P<id>\d+) (?P<name>[^|]+?) \| Kontinent [^|]+ \| "
    r"0,0 = (?P<x0>-?[\d.]+), (?P<y0>-?[\d.]+) \| 1,1 = (?P<x1>-?[\d.]+), (?P<y1>-?[\d.]+) \| Grösse (?P<w>[\d.-]+) x (?P<h>[\d.-]+)",
    re.M)


def parse(text):
    """Alle KARTE-Zeilen -> {Karten-ID: Zeile für forever_karten.csv}. Die letzte Messung pro Karte gilt."""
    rows = {}
    for m in LINE.finditer(text.replace('\\"', '"')):
        x0, y0, x1, y1 = (float(m.group(k)) for k in ("x0", "y0", "x1", "y1"))
        rows[m.group("id")] = {
            "karte": m.group("id"), "name": m.group("name").strip(),
            "a0": f"{y0:.2f}", "b0": f"{x0:.2f}", "a1": f"{y1:.2f}", "b1": f"{x1:.2f}",
            "quelle": f"Testlog KARTE vom {m.group('datum')}2026 (C_Map.GetWorldPosFromMapPos) · Grösse {m.group('w')} x {m.group('h')} Yards",
            "status": "exakt"}
    return rows


def read_rows():
    if not os.path.exists(CSV_PATH):
        return []
    with open(CSV_PATH, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))


def write_rows(rows):
    with open(CSV_PATH, "w", encoding="utf-8-sig", newline="") as f:
        f.write(";".join(FIELDS) + "\r\n")
        for r in sorted(rows, key=lambda r: int(r["karte"])):
            f.write(";".join(str(r.get(k, "")).replace(";", ",") for k in FIELDS) + "\r\n")


def check_rxp(tag, row):
    """Vergleicht RXPs Weltkoordinaten mit seinen Kommentar-Koordinaten auf dieser Karte."""
    files = subprocess.run(["git", "-C", RXP, "ls-tree", "-r", "--name-only", tag, "Guides/"],
                           capture_output=True, text=True).stdout.split()
    files = [f for f in files if "forever" in f.lower() and f.endswith(".lua")]
    a0, b0, a1, b1 = (float(row[k]) for k in ("a0", "b0", "a1", "b1"))
    pat = re.compile(r"\.goto " + row["karte"] + r"/1,(-?[\d.]+),(-?[\d.]+)[^\n]*?--c:[^,\n]+,([\d.]+),([\d.]+)")
    diffs = []
    for f in files:
        src = subprocess.run(["git", "-C", RXP, "show", f"{tag}:{f}"], capture_output=True, text=True).stdout
        for m in pat.finditer(src):
            a, b, cx, cy = (float(v) for v in m.groups())
            x = (a - a0) / (a1 - a0) * 100
            y = (b - b0) / (b1 - b0) * 100
            diffs.append(max(abs(x - cx), abs(y - cy)))
    if not diffs:
        return "keine RXP-Punkte mit Kommentar auf dieser Karte"
    return (f"{len(diffs)} RXP-Punkte: Abweichung Kommentar zu Forever-Karte "
            f"Median {statistics.median(diffs):.2f} %, max {max(diffs):.2f} %")


def main():
    if len(sys.argv) < 2:
        raise SystemExit(USAGE)
    text = open(sys.argv[1], encoding="utf-8", errors="replace").read()
    tag = sys.argv[2] if len(sys.argv) > 2 else None
    found = parse(text)
    if not found:
        print("Keine KARTE-Zeilen gefunden.")
        return
    rows = {r["karte"]: r for r in read_rows()}
    for mid, row in sorted(found.items(), key=lambda kv: int(kv[0])):
        old = rows.get(mid)
        rows[mid] = row
        note = "neu" if not old else ("ersetzt Schätzung" if old.get("status", "").startswith("geschätzt") else "aktualisiert")
        msg = f"Karte {mid} {row['name']}: a0={row['a0']} b0={row['b0']} a1={row['a1']} b1={row['b1']} ({note})"
        if tag:
            msg += " | " + check_rxp(tag, row)
        print(msg)
    write_rows(list(rows.values()))
    print("geschrieben:", os.path.relpath(CSV_PATH, ROOT))


if __name__ == "__main__":
    main()
