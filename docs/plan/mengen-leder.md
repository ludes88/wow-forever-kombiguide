# Mengenmodell Leder (erzeugt von `tools/plan_mengen.py`)

Eingabe: `data/kombi/modell_leder.csv`. Nicht von Hand ändern, sondern die Eingabe anpassen und neu erzeugen.

## Annahmen

- Bestand am Start: 8 Leichtes Leder, 13 Verdorbene Lederfetzen (Testlog 13.10. 22:42).
- Kills je Quest-Gegenstand: 2 (Annahme). Gemessen: Quest 748 am 13.10.: 14 Wölfe für 6 Pfoten (2,3), 6 Ebenenschreiter für 4 Krallen (1,5).
- Jede Haut gibt genau 1 Gegenstand (Testlog 13.10., 21 von 21 Häuten).
- Anteile Leder/Fetzen/Haut pro Zeile in der Eingabe, mit Quelle. Mulgore Stufe 5–8 gemessen (8 von 21 Leder), sonst MetaForge (Vanilla-Daten) als Näherung.
- «Basis» = Quests, die die Route sicher macht. «Option» = Kürschnerbarkeit ungeprüft oder optionale Grind-Schritte.
- Nicht im Modell: Tiere, die nebenbei sterben, Light Hide und Medium Leather ab Stufe 15, AH-Käufe.

## Abschnitte

| Abschnitt | bis | Kills Basis | Leder Basis | Fetzen Basis | Kills Option | Leder Option | Leder kumuliert (Basis) | mit Optionen |
|---|---|---|---|---|---|---|---|---|
| A | Thunder Bluff, Ruhestein (RXP-Label TBHome) | 30 | 11.4 | 18.6 | 19 | 7.2 | 19 | 27 |
| B | Ende Mulgore (RXP-Label WildManeTurnIn) | 25 | 10.0 | 15.0 | 15 | 6.0 | 29 | 43 |
| C | Brachland bis etwa Stufe 15 (Ausblick v0.3) | 70 | 42.0 | 24.5 | 0 | 0.0 | 71 | 85 |

## Ziele im Kombi-Guide (Basis, abgerundet)

- Abschnitt A, Thunder Bluff, Ruhestein (RXP-Label TBHome): **19 Leichtes Leder** im Inventar (Bank zählt mit)
- Abschnitt B, Ende Mulgore (RXP-Label WildManeTurnIn): **29 Leichtes Leder** im Inventar (Bank zählt mit)
- Abschnitt C, Brachland bis etwa Stufe 15 (Ausblick v0.3): **71 Leichtes Leder** im Inventar (Bank zählt mit)

## Vergleich mit dem Bedarf

| Bedarf | Leder | Lücke (Basis) | Lücke mit Optionen | AH-Wert der Lücke (Basis) |
|---|---|---|---|---|
| LW 125 und VZ im Mittel 125 | 416 | 345 | 331 | 1g 72s 30c bis 2g 34s 33c |
| VZ 130 mit 90 % Sicherheit | 488 | 417 | 403 | 2g 8s 30c bis 2g 83s 29c |
| VZ 150 mit 90 % Sicherheit | 644 | 573 | 559 | 2g 86s 30c bis 3g 89s 37c |

Fetzen: erwartet 71 von 100, Lücke 29 (AH-Wert 7s 23c bis 8s 9c).

## Zeilen

| Abschnitt | Quest | Ziel | Kreatur | Kills | Art | Quelle |
|---|---|---|---|---|---|---|
| A | 756 | Stalker Claws (6) | Prairie Stalker | 12 | Quest | Anzahl: RXP v4.11.23 (Kommentar) · kürschnerbar: Testlog 13.10. · Anteile: Testlog 13.10. (Mulgore, 8 Leder und 13 Fetzen aus 21 Häuten) |
| A | 756 | Cougar Claws (6) | Flatland Cougar | 12 | Quest | wie oben |
| A | 766 | Prairie Wolf Heart, Flatland Cougar Femur, Plainstrider Scale (je 1) | Prairie Wolf, Flatland Cougar, Adult Plainstrider | 6 | Quest | wie oben |
| A | 761 | Trophy Swoop Quill (8), Swoop Gizzard (1) | Wiry Swoop, Swoop | 18 | Option: kürschnerbar ungeprüft | Anzahl: RXP · im Testlog 13.10. nie gekürschnert |
| A | 96130 | Chakuyak's Pelt (1) | Chakuyak | 1 | Option: kürschnerbar ungeprüft | Anzahl: RXP · Kreatur-ID: AHledger |
| B | 861 | Flatland Prowler Claw (4) | Flatland Prowler | 8 | Quest | Anzahl: RXP · Anteile: MetaForge Kodo Calf (Stufe 7–8: 40 % Leder, 60 % Fetzen), Näherung |
| B | 759 | Prairie Alpha Tooth (8) | Prairie Wolf Alpha | 16 | Quest | wie oben |
| B | 776 | Horn of Arra'chea (1) | Arra'chea | 1 | Quest | wie oben · kürschnerbar ungeprüft |
| B | Grind | optionale RXP-Schritte «Grind to …/6500xp» in Nord-Mulgore (Annahme 15 Kills) | Prairie Wolf Alpha, Prairie Stalker, Flatland Cougar, Plainstrider | 15 | Option: Grind | Kills: Annahme, keine Quelle |
| C | 844 | Plainstrider Beak (7) | Greater Plainstrider, Fleeting Plainstrider | 14 | Quest | Anzahl: RXP · Anteile: MetaForge Zhevra Runner (Stufe 13–14), Näherung |
| C | 869 | Raptor Head (12) | Sunscale Lashtail, Sunscale Screecher | 24 | Quest | wie oben |
| C | 845 | Zhevra Hooves (4) | Zhevra Runner | 8 | Quest | wie oben |
| C | 821 | Plainstrider Kidney (5) | Greater Plainstrider, Fleeting Plainstrider | 10 | Quest | wie oben · zum Teil erst nach Stufe 15 |
| C | 903, 821 | Prowler Claws (7) und Savannah Lion Tusk (5), gleiche Kreatur | Savannah Prowler | 14 | Quest | wie oben · zum Teil erst nach Stufe 15 |
