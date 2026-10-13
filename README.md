# WoW Forever: Kombi-Guide und Berufe

Ein RestedXP-Guide für Stufe 1–22 (Horde, Tauren-Druide), der RXPs Gratis-Route mit Berufsschritten verbindet: Kräuterkunde und Kürschnerei bis etwa Stufe 15, danach Lederverarbeitung und Verzauberkunst bis 150, dazu Fischen und Kochen.

Stand 13.10.2026: Kombi-Guide v0.1 im Spiel getestet (Forever-Beta, RestedXP v4.11.13), v0.1.1 gebaut. Testberichte in `docs/tests/`.

## Inhalt

- `addons/KombiTestlog/`: Notizen und Testprotokoll im Spiel (`/tl hilfe`)
- `addons/RXPGuides_Kombi/`: eigene RXP-Guides, zurzeit der Test «Vorquests Höhlen des Wehklagens»
- `data/kombi/plan.csv`: Plan-Tabelle der Berufsschritte (lässt sich in Excel öffnen)
- `data/karten/forever_karten.csv`: Kartenecken für die Koordinaten-Umrechnung
- `docs/Weg-A_Best-Practice.md`: Aufbau, RXP-Syntax, Update-Ablauf, Risiken, Berufsdaten, Testplan
- `docs/vorgehen.md`: Arbeitsweise, Datenkette, Versionen
- `tools/`: Kombi-Guide bauen (`build_kombi.py`), Prüfen, Testlauf
- `data/rechnung/`: Rechnung Lederverarbeitung und Verzauberkunst

## Einbau ins Spiel (Beta)

Die Ordner aus `addons/` und den gebauten Ordner `build/RXPGuides_KombiGuide/` nach `World of Warcraft\_classic_beta_\Interface\AddOns\` kopieren, neben `RXPGuides`. Den Kombi-Guide baut `python3 tools/build_kombi.py <RXP-Version>`.

## Herkunft

Die Guide-Schritte stammen aus den RestedXP-Gratis-Guides (https://github.com/RestedXP/RXPGuides, CC BY-NC-SA 4.0) und sind bearbeitet. Siehe `LICENSE-NOTES.md`.
