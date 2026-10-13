# Mengenmodell Leder: wie viel Leichtes Leder die RXP-Route bis zum Berufswechsel (etwa Stufe 15) bringt
#
# Aufruf: python3 tools/plan_mengen.py [Bericht.md]      (Standard: docs/plan/mengen-leder.md)
# Eingabe: data/kombi/modell_leder.csv (eine Zeile pro Quest mit Tieren; Anzahl aus den RXP-Kommentaren)
#
# Rechnung pro Zeile: Kills = Stück × Kills je Stück; Leder = Kills × Leder-Anteil (jede Haut gibt 1 Gegenstand, Testlog 13.10.).
# «Quest» zählt zur Basis; «Option: …» (z. B. Kürschnerbarkeit ungeprüft, optionales Grinden) steht getrennt daneben.
# Alle Annahmen stehen in der Eingabedatei und unten in KONSTANTEN; der Bericht nennt sie.
import csv, math, os, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "docs", "plan", "mengen-leder.md")

# KONSTANTEN mit Quelle
START = {"leder": 8, "fetzen": 13}          # Testlog 13.10. 22:42 (Tauren-Druide, Stufe 7, Kürschnerei 22)
BEDARF = [("LW 125 und VZ im Mittel 125", 416), ("VZ 130 mit 90 % Sicherheit", 488), ("VZ 150 mit 90 % Sicherheit", 644)]
FETZEN_BEDARF = 100                           # Rechnung 13.10. (Best Practice §1)
PREIS_LEDER = (0.50, 0.68)                    # Silber, AHledger Horde US Normal/PvP Median 12.10. (data/rechnung/Preise.csv)
PREIS_FETZEN = (0.25, 0.28)                   # dito
KILLS_JE_STUECK_GEMESSEN = "Quest 748 am 13.10.: 14 Wölfe für 6 Pfoten (2,3), 6 Ebenenschreiter für 4 Krallen (1,5)"


def read(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))


def silber(s):
    g, r = divmod(round(s * 100), 10000)
    sv, k = divmod(r, 100)
    parts = []
    if g: parts.append(f"{g}g")
    if sv: parts.append(f"{sv}s")
    if k or not parts: parts.append(f"{k}c")
    return " ".join(parts)


rows = read(os.path.join(ROOT, "data", "kombi", "modell_leder.csv"))
sections = []
for r in rows:
    if not sections or sections[-1]["id"] != r["abschnitt"]:
        sections.append({"id": r["abschnitt"], "bis": r["bis"], "rows": []})
    sections[-1]["rows"].append(r)

lines = ["# Mengenmodell Leder (erzeugt von `tools/plan_mengen.py`)", "",
         "Eingabe: `data/kombi/modell_leder.csv`. Nicht von Hand ändern, sondern die Eingabe anpassen und neu erzeugen.", "",
         "## Annahmen", "",
         f"- Bestand am Start: {START['leder']} Leichtes Leder, {START['fetzen']} Verdorbene Lederfetzen (Testlog 13.10. 22:42).",
         f"- Kills je Quest-Gegenstand: 2 (Annahme). Gemessen: {KILLS_JE_STUECK_GEMESSEN}.",
         "- Jede Haut gibt genau 1 Gegenstand (Testlog 13.10., 21 von 21 Häuten).",
         "- Anteile Leder/Fetzen/Haut pro Zeile in der Eingabe, mit Quelle. Mulgore Stufe 5–8 gemessen (8 von 21 Leder), sonst MetaForge (Vanilla-Daten) als Näherung.",
         "- «Basis» = Quests, die die Route sicher macht. «Option» = Kürschnerbarkeit ungeprüft oder optionale Grind-Schritte.",
         "- Nicht im Modell: Tiere, die nebenbei sterben, Light Hide und Medium Leather ab Stufe 15, AH-Käufe.", "",
         "## Abschnitte", "",
         "| Abschnitt | bis | Kills Basis | Leder Basis | Fetzen Basis | Kills Option | Leder Option | Leder kumuliert (Basis) | mit Optionen |",
         "|---|---|---|---|---|---|---|---|---|"]
cum = float(START["leder"]); cum_opt = cum; cum_f = float(START["fetzen"])
targets = []
for s in sections:
    kb = lb = fb = ko = lo = 0.0
    for r in s["rows"]:
        kills = float(r["stueck"]) * float(r["kills_je_stueck"])
        leder, fetzen = kills * float(r["leder_anteil"]), kills * float(r["fetzen_anteil"])
        if r["art"] == "Quest":
            kb += kills; lb += leder; fb += fetzen
        else:
            ko += kills; lo += leder
    cum += lb; cum_opt += lb + lo; cum_f += fb
    targets.append((s["id"], s["bis"], math.floor(cum)))
    lines.append(f"| {s['id']} | {s['bis']} | {kb:.0f} | {lb:.1f} | {fb:.1f} | {ko:.0f} | {lo:.1f} | {cum:.0f} | {cum_opt:.0f} |")

lines += ["", "## Ziele im Kombi-Guide (Basis, abgerundet)", ""]
for sid, bis, t in targets:
    lines.append(f"- Abschnitt {sid}, {bis}: **{t} Leichtes Leder** im Inventar (Bank zählt mit)")

lines += ["", "## Vergleich mit dem Bedarf", "",
          "| Bedarf | Leder | Lücke (Basis) | Lücke mit Optionen | AH-Wert der Lücke (Basis) |", "|---|---|---|---|---|"]
for name, need in BEDARF:
    gap, gap_o = max(0, need - cum), max(0, need - cum_opt)
    lines.append(f"| {name} | {need} | {gap:.0f} | {gap_o:.0f} | {silber(gap * PREIS_LEDER[0])} bis {silber(gap * PREIS_LEDER[1])} |")
fgap = max(0, FETZEN_BEDARF - cum_f)
lines += ["", f"Fetzen: erwartet {cum_f:.0f} von {FETZEN_BEDARF}, Lücke {fgap:.0f} (AH-Wert {silber(fgap * PREIS_FETZEN[0])} bis {silber(fgap * PREIS_FETZEN[1])}).",
          "", "## Zeilen", "", "| Abschnitt | Quest | Ziel | Kreatur | Kills | Art | Quelle |", "|---|---|---|---|---|---|---|"]
for r in rows:
    kills = float(r["stueck"]) * float(r["kills_je_stueck"])
    lines.append(f"| {r['abschnitt']} | {r['quest']} | {r['ziel']} | {r['kreatur']} | {kills:.0f} | {r['art']} | {r['quelle']} |")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8").write("\n".join(lines) + "\n")
for sid, bis, t in targets:
    print(f"Ziel {sid} ({bis}): {t} Leichtes Leder")
print(f"Basis bis Abschnitt {sections[-1]['id']}: {cum:.0f} Leder, mit Optionen {cum_opt:.0f}; Bericht: {os.path.relpath(OUT, ROOT)}")
