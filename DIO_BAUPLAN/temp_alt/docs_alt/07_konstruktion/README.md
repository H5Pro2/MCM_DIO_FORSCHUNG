# KONSTRUKTION

Dieser Ordner ist ab jetzt die Referenz fuer den Wiederaufbau der MCM-Regulation.

Wichtig:

- Der alte Projektordner `C:\Users\TV\Documents\24.05 v1 MCM_Trading_Brain` ist nur die Quelle, aus der die Verdrahtung extrahiert wurde.
- Der alte Code selbst ist nicht die Referenz, die blind kopiert werden soll.
- Referenz ist die hier abgelegte Konstruktion: Ablauf, Datenvertraege, Invarianten und Pruefpunkte.
- Ziel ist, das organische Regulationsverhalten wiederherzustellen, ohne alte Monolith-Struktur oder alte Fehler zu uebernehmen.

Zweck:

- technische Bauanleitung fuer den Regulationspfad
- kontrollierte Rekonstruktion nach dem Funktionssplit
- Schutz gegen Refactor-Fehler wie Overtrading, `allow_plan`-Bypass oder Motorik aus Gegensignalen
- klare Trennung zwischen Hypothese, innerer Regulation, Gate und Handlung

Kanonische Dateien:

- `REGULATIONS_KONSTRUKTION.md`
  Beschreibt den Regulationsfluss von Marktdaten bis Entry/Non-Action als Zielverdrahtung.

- `FUNKTIONALE_VERDRAHTUNG.md`
  Listet die wichtigen Funktionsrollen, Datenuebergaben und heutigen Zielmodule.

- `REGULATIONS_REKONSTRUKTION_CHECKLISTE.md`
  Pruefpunkte, um den aktuellen Code gegen die Konstruktion zu validieren.

- `AKTUELLER_REGULATIONS_ABGLEICH.md`
  Aktueller Abgleich zwischen Konstruktion und Funktionssplit: vorhandene
  Pfade, Datenvertraege, Risiken und naechste Pruefpunkte.

- `ENTMECHANISIERUNG_PLAN.md`
  Plan fuer den gezielten Rueckbau ueberladener Core-Daten, starrer Gates und
  indirekter Wenn-Dann-Logik. Ziel ist weichere MCM-Feldmodulation statt
  mechanischer Freigabe-/Sperrketten.

- `ENTMECHANISIERUNG_ABGLEICH.md`
  Konkreter Ist-Abgleich der aktuellen Module gegen den Rueckbauplan:
  Core-Werte, Perception, Gates, Trade-Plan, Hypothesenlernen und priorisierte
  erste Umbaustellen.

Leitsatz:

Nicht der alte Code ist das Ziel. Ziel ist die extrahierte MCM-Mechanik:

`Wahrnehmung -> Feld -> Verarbeitung -> Fuehlen -> Denken -> Meta-Regulation -> decision_tendency -> Gate -> Handlung nur bei act -> Outcome -> Rueckkopplung`
