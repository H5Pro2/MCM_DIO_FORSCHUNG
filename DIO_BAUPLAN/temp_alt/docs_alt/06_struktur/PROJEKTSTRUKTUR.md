# PROJEKTSTRUKTUR

Ziel dieser Datei:
- Zielstruktur des Projekts festhalten
- Verantwortlichkeiten der Module klar trennen
- unterscheiden zwischen Brain-Mechanik, Runtime, Trading, Speicher, Debug und Dokumentation
- Refactoring schrittweise fuehren, ohne DIOs Mechanik zu brechen

Stand nach Refactoring Phase 4bb:
Die wichtigsten Brain-Zustandsbloecke sind aus `MCM_Brain_Modell.py`
ausgelagert. `MCM_Brain_Modell.py` ist weiterhin die Runtime-Bruecke, aber
nicht mehr der alleinige Besitzer aller Mechaniken.

Aktueller Checkpoint nach Datei-Aufraeumung:
Interne Imports wurden von Root-Kompatibilitaetswrappern auf echte Zielmodule
umgestellt. Die alten `legacy_wrappers/`-Importbruecken wurden nach
erfolgreichem isoliertem Backtest-Smoke entfernt. Das reduziert sichtbare
Doppeldateien und verhindert, dass alte Importpfade wieder versehentlich als
aktive Struktur gelesen werden.
Auch die Tests verwenden keine kuenstlich injizierten Root-Wrapper fuer
`bot_engine` mehr.
Zusaetzlich wurde die Restart-Recovery fuer offene Live-Orders und aktive
Positionen nach `bot_engine/restart_recovery.py` ausgelagert.
Die Runtime-Thread- und Queue-Steuerung liegt jetzt in
`bot_engine/runtime_thread.py`.
Die Live-Market-Dedupe-Pruefung liegt jetzt in
`bot_engine/market_packets.py`.
Der Runtime-Packet-Action-Cycle liegt jetzt in
`bot_engine/runtime_processing.py`.
Der Runtime-Entry-Zustandsaufbau liegt jetzt in
`core/runtime_entry.py`.
Die Review-/Experience-Feedback-Berechnung liegt jetzt in
`core/review_feedback.py`.
Die Felt-State-Berechnung liegt jetzt in `core/felt_state.py`.
Innerhalb von `core/felt_state.py` ist die Eingangsachsen-Sammlung jetzt in
`_collect_felt_input_axes` getrennt, damit die eigentliche Felt-Verdichtung
schrittweise weiter zerlegt werden kann.
Die Areal-/Feldkontaktverdichtung liegt dort zusaetzlich in
`_compute_felt_areal_axes`.
Risiko-, Gelegenheits- und Konfliktverdichtung liegen dort in
`_compute_felt_valence_axes`.
Druck-, Stabilitaets-, Alignment- und Spannungsursachenverdichtung liegen
dort in `_compute_felt_regulation_axes`.
Dieser Regulationsblock ist intern weiter geteilt in Kernregulation,
Spannungsursachen und Beobachtungsbedarf.
Label- und Rueckgabeaufbau liegen in `_resolve_market_feel_state` und
`_build_felt_state_payload`; `resolve_felt_state` ist nur noch
Orchestrator.
Die Runtime-Followup-Schicht fuer Idle-Schritte, Flush und Market-Nachlauf
liegt jetzt in `bot_engine/runtime_followup.py`.
Die Live-Boot-Recovery-Fassade liegt jetzt in `bot_engine/live_recovery.py`.
Die Idle-Phasenklassifikation liegt jetzt in
`bot_engine/idle_thinking_protocol.py`; `bot.py` haelt nur noch
Kompatibilitaetswrapper.
Der Entry-Attempt-Kontextverdichter liegt jetzt in
`bot_engine/entry_attempt_context.py`.
Die Positions-Interventionsauswertung liegt jetzt in
`bot_engine/position_intervention.py`.
Die Exit-Kandidaten-Beobachtung liegt jetzt in
`bot_engine/exit_candidate_observe.py`.
Die Zielerwartungs-Auswertung liegt jetzt in
`bot_engine/target_expectation.py`.
Die gereifte Exit-Signal-Auswertung liegt jetzt in
`bot_engine/matured_exit.py`.
Der aktive Positionshandler liegt jetzt in `bot_engine/active_position.py`.
Der Pending-Entry-Handler liegt jetzt in `bot_engine/pending_entry.py`.
Der Entry-Attempt-Handler liegt jetzt in `bot_engine/entry_attempt.py`.
Die innere Handlungsfreigabe fuer Entry-Motorik liegt in
`bot_gates/entry_decision.py`: Impuls und Bereichskontakt duerfen dort
Wahrnehmung und Vorreaktion vorbereiten, aber die Order-Motorik braucht eine
MCM-getragene innere Zustimmung. Innere Unklarheit wird als Beobachtung und
Hypothesenreifung behandelt. Nicht-Handlung ist dabei eine eigene
Konsequenzspur und kein verpasster Trade.
Die Strategie-Verdichtung aus bestaetigten hypothetischen Trades liegt
ebenfalls in dieser Gate-Schicht: `strategy_confirmation`,
`strategy_rejection` und `strategy_trust_bearing` verbinden beobachtete
Hypothesen mit realer Motorik.
Ein isolierter Backtest-Smoke nach dieser Auslagerung ist erfolgreich
durchgelaufen: Runtime-Thread, Feed-Fenster, Queue-Idle, Memory-Save und
Debug-Flush funktionieren mit der neuen Bot-/Engine-Aufteilung.

Grobe Einordnung:
Die strukturelle Auslagerung liegt aktuell bei etwa 99 %. `bot.py` liegt bei
etwa 1064 Zeilen und ist groesstenteils Fassade/Kompatibilitaetsschicht.
`bot_engine/` umfasst aktuell 29 Python-Module. Die Zielmodule stehen, viele
Mechaniken sind ausgelagert, aber mehrere zentrale Orchestrierungs- und
Bot-Seiteneffekt-Bloecke liegen noch im Brain oder in grossen Core-Funktionen.
`core/felt_state.py::resolve_felt_state` ist durch die internen Schnitte auf
etwa 26 Zeilen reduziert; der groesste Felt-State-Restblock ist jetzt
`_compute_felt_tension_cause_axes`.

Hinweis zu Kompatibilitaetsfassaden:
Einige Imports oder Wrapper in `bot.py` koennen statisch ungenutzt wirken,
werden aber als externe Patch-/Kompatibilitaetspunkte gebraucht. Beispiel:
`bot.read_memory_state` wird von Tests direkt gepatcht und bleibt deshalb
bewusst auf Modulebene verfuegbar.

Groesste Restbloecke:

- `core/decision_regulation.py::build_meta_regulation_state`
- Runtime-Entry-/Result-Orchestrierung in `MCM_Brain_Modell.py`
- Restliche Formsymbol-Wrapper und Runtime-Anbindung in `MCM_Brain_Modell.py`
- Felt-State in `MCM_Brain_Modell.py`
- Experience-Orchestrierung in `MCM_Brain_Modell.py`
- Review-/Runtime-Feedback in `MCM_Brain_Modell.py`

Aktueller Messpunkt nach Felt-State-Schnitt:

- `core/decision_regulation.py::build_meta_regulation_state`: ca. 1551 Zeilen
- `trading/trade_stats.py::_compact_context`: ca. 705 Zeilen
- `core/mcm_field.py::build_active_mcm_contact_state`: ca. 597 Zeilen
- `core/form_symbol_orchestration.py::build_form_symbol_state`: ca. 582 Zeilen
- `trading/trade_stats.py::on_exit`: ca. 558 Zeilen
- `trading/trade_plan.py::derive_trade_plan_from_brain`: ca. 517 Zeilen

Naechster strukturell sinnvoller Zielblock ist die Meta-Regulation, weil dort
die hoechste Komplexitaet und das hoechste Risiko fuer Scope-/Initialisierungs-
Fehler liegt.
Erster Schnitt dort ist umgesetzt: Trust-Return-/Gedankenbestaetigung liegt in
`_build_trust_return_state`.

Echte Implementierungen liegen jetzt in:

- `core/active_context.py`
- `core/experience_space.py`
- `core/felt_state.py`
- `core/inner_context.py`
- `core/inner_pattern.py`
- `core/thought_memory.py`
- `core/form_symbol_orchestration.py`
- `memory/thought_memory_store.py`
- `core/form_language.py`
- `core/hypothesis_learning.py`
- `core/brain_factory.py`
- `core/runtime.py`
- `core/runtime_bridge.py`
- `core/runtime_tendency.py`
- `core/runtime_snapshot.py`
- `core/runtime_commit.py`
- `core/runtime_field_state.py`
- `core/review_feedback.py`
- `core/strategic_window.py`
- `core/temporal_perception.py`
- `core/perception.py`
- `core/neurochemistry.py`
- `core/mcm_field.py`
- `core/decision_regulation.py`
- `memory/form_symbol_memory.py`
- `trading/trade_plan.py`
- `bot_engine/active_position.py`
- `bot_engine/entry_attempt.py`
- `bot_engine/entry_attempt_context.py`
- `bot_engine/exit_candidate_observe.py`
- `bot_engine/live_recovery.py`
- `bot_engine/matured_exit.py`
- `bot_engine/pending_entry.py`
- `bot_engine/position_intervention.py`
- `bot_engine/target_expectation.py`
- `bot_engine/state_initialization.py`
- `bot_engine/regulation_snapshot.py`
- `bot_engine/restart_recovery.py`
- `bot_engine/runtime_followup.py`
- `bot_engine/runtime_thread.py`
- `bot_engine/visualization_snapshots.py`
- `bot_engine/market_packets.py`
- `debug_tools/writers.py`
- `debug_tools/protocols.py`
- `debug_tools/visualization.py`
- `debug_tools/field_snapshots.py`

Restrolle von `MCM_Brain_Modell.py`:

- Runtime-Bruecke zwischen Bot, MCM-Feld, Wahrnehmung, Regulation und Ergebnis
- Funktionen mit starken Seiteneffekten oder Bot-Zustandsmutation
- lokale Leseschichten fuer Bot-Zustand, bevor Daten an Core-Verdichtung
  uebergeben werden
- Base-Summary-Aufbau fuer Experience-Episoden, solange Bot-Fallbacks noch
  benoetigt werden
- Kompatibilitaet fuer bestehende Imports aus `bot.py` und Gate-Funktionen

Legacy-Wrapper:
Die alten `legacy_wrappers/`-Dateien wurden entfernt. Es bleiben nur bewusste
Kompatibilitaetspunkte dort, wo sie wirklich gebraucht werden, zum Beispiel
`bot.read_memory_state` als Patchpunkt fuer Tests und externe Aufrufer.

---

# Zielstruktur

```text
core/
  active_context.py
  brain_factory.py
  experience_space.py
  inner_context.py
  inner_pattern.py
  mcm_field.py
  neurochemistry.py
  perception.py
  temporal_perception.py
  hypothesis_learning.py
  thought_memory.py
  form_language.py
  runtime.py
  runtime_bridge.py
  runtime_tendency.py
  runtime_snapshot.py
  runtime_commit.py
  runtime_field_state.py
  strategic_window.py
  decision_regulation.py

trading/
  trade_plan.py
  order_logic.py
  backtest_runtime.py
  live_runtime.py

bot_engine/
  active_position.py
  action_context.py
  entry_attempt.py
  entry_attempt_context.py
  exit_candidate_observe.py
  execution_outcomes.py
  execution_paths.py
  feed_runtime.py
  live_recovery.py
  market_packets.py
  market_perception.py
  matured_exit.py
  pending_entry.py
  position_intervention.py
  regulation_snapshot.py
  restart_recovery.py
  runtime_followup.py
  runtime_processing.py
  runtime_thread.py
  runtime_timing.py
  state_initialization.py
  target_expectation.py
  visualization_snapshots.py

memory/
  memory_state.py
  form_symbol_memory.py
  thought_memory_store.py

debug_tools/
  writers.py
  protocols.py
  field_snapshots.py
  visualization.py
  debug_reader.py

docs/
  00_regeln/
  01_plan/
  02_status/
  03_mechanik/
  04_berichte/
  05_gui/
  06_struktur/
  07_konstruktion/
  documente/

files/
  BILDER/
```

Hinweis:
`debug/` bleibt Runtime-Ausgabeordner fuer `debug_lauf_*`. Code liegt bewusst
in `debug_tools/`, damit Debug-Reset oder Archivierung keine Python-Module
loescht.

---

# Modulverantwortung

## core

`core` ist der Zielort fuer DIOs Brain-Mechanik.

- `active_context.py`: aktive Kontextspur, Replay-Impuls, Decay, Nervensystem-Modulation und Quellenwahl aus Inner-Cluster/Temporal-State
- `experience_space.py`: Experience-Bearing, neurochemischer Experience-Effekt, Reward-Delta, Similarity-Axes, Link-Buckets, Outcome-Protokoll, Episode-Links, Episode-Felt-Auswertung, Summary-Anreicherung, In-Trade-Experience-Verdichtung, Episode-Review-Berechnung und affektives Strukturprofil
- `inner_context.py`: innerer Kontext-Cluster-State, Vektorbildung, Cluster-Memory, Trust/Score/Outcome-Spuren
- `inner_pattern.py`: innere Feldmuster-Identitaet, Wiedererkennung, Stabilitaetsstreak und Pattern-Signatur
- `mcm_field.py`: MCM-Feldzugriff, neuronale Grundstruktur, aktiver MCM-Kontakt, affektive Kontextmodulation
- `brain_factory.py`: Aufbau des MCM-Brain-Objektgraphs mit injizierten Klassen
- `neurochemistry.py`: neurochemische Zustandsbildung und MCM-Spannungsachse
- `perception.py`: Weltzustand, aeussere Wahrnehmung, Processing und bewusste Wahrnehmung
- `temporal_perception.py`: Zeit-/Raumzeit-Wahrnehmung, Nachhall, Gegenwart, Erinnerung und Zukunftstiefe
- `hypothesis_learning.py`: beobachtete Hypothesen, Vertrauen, Frust, Distanz, Moeglichkeitsreife
- `thought_memory.py`: Gedanken-Memory, Gedankenfamilien, atomisches Schreiben
- `form_language.py`: DIO-Formsprache, semantische Verdichtung, Formsymbol-Helfer, Formsymbol-Identitaet, Formsymbol-Basisqualitaet, Formsymbol-Objektentkopplung, Formsymbol-Lernkern, Compound-Form-Berechnung, Formsymbol-Item-Statistik, semantische Formverdichtung und Variantenfamilien-Auswertung
- `runtime.py`: Runtime-Klasse fuer Tick, Advance, Impulse und Snapshot-Zustand; Brain-Mechanik wird injiziert
- `runtime_bridge.py`: Bridge-Funktionen fuer Runtime-Erzeugung, Idle-Advance und Markt-Tick; Compute/Apply werden injiziert
- `runtime_tendency.py`: lesende Runtime-Tendenz-Ansicht fuer Gate- und Entry-Entscheidungen
- `runtime_snapshot.py`: Runtime-Snapshot, Pipeline-Snapshot, Decision-State, neuronale Felt-Zusammenfassung und Active-Context-Signalformung
- `runtime_commit.py`: klar getrennte Runtime-Commit-Schritte fuer Wahrnehmungs-Advance, Snapshot-State, sichtbare/interne Episode, Experience-Space-Refresh und Active-Context
- `runtime_field_state.py`: Feldlast, Feldstabilitaet, Survival-Pressure, Regulatory-Load, Action-Capacity und Recovery-Need aus Runtime-/Bot-Zustand
- `strategic_window.py`: strategische Rueckblickwahrnehmung, Bereichskandidaten, Area-Bearing, Replay-Fit, Spacetime-Fit und Patience-Werte
- `decision_regulation.py`: Thought-State, Meta-Regulation, gekapselte Feldregulations-Berechnung, Formsymbol-Lernregulation, Orientierungsberechnung und Strukturaktionsbewertung

## trading

`trading` ist der Zielort fuer Handelsumsetzung und Laufzeit.

- `trade_plan.py`: Entry-/SL-/TP-/RR-Planung ohne Orderausfuehrung
- `order_logic.py`: Live-Order-Funktionen
- `backtest_runtime.py`: Backtest-Feed und Bot-Lauf
- `live_runtime.py`: Live-Startpunkt

## bot_engine

`bot_engine` enthaelt Bot-nahe Mechaniken und technische Bot-Bausteine, die
nicht direkt in `bot.py` bleiben muessen.

- `active_position.py`: aktiver Positionshandler, Positions-Update, Exit-
  Engine-Anbindung, Live-Exit-Bestaetigung und gereifter Exit
- `entry_attempt.py`: Entry-Attempt-Handler, Entry-Decision, Value-Gate,
  Live-Order-Submit und Delegation an Entry-Finalizer
- `entry_attempt_context.py`: Entry-Attempt-Kontextverdichtung fuer
  Episode/Memory, inklusive Field-, Experience-, Trade-Plan- und Signalachsen
- `exit_candidate_observe.py`: beobachtende Exit-Kandidatenbewertung,
  Confirmation-Score, Debugprotokoll und Episode-Markierung ohne Exit-Ausfuehrung
- `state_initialization.py`: initialer Bot-Zustand, Komponentenaufbau und
  Startwerte ohne Marktentscheidung
- `regulation_snapshot.py`: Bot-Regulationszustand und Delta-Berechnung fuer
  Tension-, Field- und Experience-Achsen
- `restart_recovery.py`: Wiederanlauf von Pending-Order oder aktiver Position
  aus einem Live-Snapshot, inklusive Episode- und Regulationszustand
- `visualization_snapshots.py`: Bot-nahe Visual-/Inner-Snapshot-Orchestrierung,
  Write-Due, Buffering und Flush
- `market_packets.py`: reine Market-/Runtime-Packet-Formung, Window-
  Normalisierung, Outer-Market-State und Live-Dedupe-Key
- `live_recovery.py`: Live-Boot-Fassade fuer Snapshot-Abfrage,
  Restart-Recovery-Ausloesung und Memory-Save nach Wiederherstellung
- `matured_exit.py`: gereifte Exit-Signal-Auswertung, Matured-Exit-Protokoll
  und Episode-Markierung ohne direkte Orderausfuehrung
- `pending_entry.py`: Pending-Entry-Handler, Live-Cancel, Live-Fill-Handoff,
  Live-/Backtest-Timeout und Backtest-Fill
- `position_intervention.py`: neuroregulatorische Auswertung offener
  Positionen, Interventionsdruck, Planvertrauen und Positionsfeldlast
- `target_expectation.py`: Zielerwartungs-Auswertung offener Positionen,
  TP-Erreichbarkeit, Erwartungsbruch, Recovery-Watch und Positionspeaks
- `runtime_followup.py`: Idle-Step, Runtime-Followup-Flush,
  Idle-Followup-Protokoll und Market-Followup ohne Marktentscheidung
- `runtime_thread.py`: technische Thread-/Queue-Steuerung, Start/Stop,
  Idle-Warten und Watchdog-Debug ohne Marktentscheidung

## memory

`memory` ist der Zielort fuer persistente Speicher.

- `memory_state.py`: Welt-/Erfahrungsspeicher
- `form_symbol_memory.py`: Formsymbolspeicher
- `thought_memory_store.py`: Gedanken- und Hypothesenspeicher

## debug_tools

`debug_tools` ist der Zielort fuer Debug-Code.

- `writers.py`: Schreibfunktionen, Pfadaufl??sung, Buffer und Laufordner
- `protocols.py`: Debug-Protokoll-Funktionen
- `field_snapshots.py`: read-only Feldtopologie-, Neuron-, Areal- und Cluster-Snapshots
- `visualization.py`: Visual-/Inner-Snapshots, Chart-Snapshot und Runtime-Regulations-Transition
- `debug_reader.py`: Kompatibilitaetsadapter zum bestehenden Debug-Reader

## docs / files

- `docs/`: aktive Markdown-Dokumentation, nach Funktion in Unterordner sortiert
- `docs/00_regeln/`: Dokumentationsregeln und Zuständigkeiten
- `docs/01_plan/`: Bauplan-Einstieg und langfristige Zielarchitektur
- `docs/02_status/`: aktueller Stand, Fixliste, Archiv und Entwicklungsuebersicht
- `docs/03_mechanik/`: Mechaniken, Variablen, Rezeptoren und MCM-Erweiterungen
- `docs/04_berichte/`: Erfahrungsberichte
- `docs/05_gui/`: GUI-Konzeption
- `docs/06_struktur/`: Projektstruktur und Refactoring-Plan
- `docs/07_konstruktion/`: Regulationskonstruktion, Verdrahtung und
  Rekonstruktionschecklisten
- `files/`: Bilder und sonstige Assets, aktuell `files/BILDER/`


---

# Entfernte Legacy-Kompatibilitaetswrapper

Die folgenden alten Importbruecken wurden nach internem Importcheck und
isoliertem Backtest-Smoke entfernt:

- `legacy_wrappers/memory_state.py` -> `memory/memory_state.py`
- `legacy_wrappers/MCM_KI_Modell.py` -> `core/mcm_model.py`
- `legacy_wrappers/trade_stats.py` -> `trading/trade_stats.py`
- `legacy_wrappers/place_orders.py` -> `trading/order_logic.py`
- `legacy_wrappers/place_orders_funktions.py` -> `trading/order_api_helpers.py`
- `legacy_wrappers/csv_feed.py` -> `trading/csv_feed.py`
- `legacy_wrappers/ph_ohlcv.py` -> `trading/exchange_data.py`
- `legacy_wrappers/bot_gate_funktions.py` -> `bot_gates/entry_decision.py`
- `legacy_wrappers/debug_reader.py` -> `debug_tools/writers.py`
- `legacy_wrappers/exit_engine.py` -> `bot_engine/exit_engine.py`
- `legacy_wrappers/mcm_core_engine.py` -> `bot_engine/mcm_core_engine.py`
- `legacy_wrappers/strukture_engine.py` -> `bot_engine/strukture_engine.py`
- `legacy_wrappers/trade_value_gate.py` -> `bot_gates/trade_value_gate.py`

Wenn spaeter externe Skripte solche alten Namen benoetigen, muessen sie
gezielt als klare API-Fassade neu angelegt werden. Der aktuelle Projektkern
arbeitet direkt mit den Paketmodulen.

---

# Refactoring-Regeln

1. Keine Grossverschiebung ohne Zwischentest.
2. Echte Codeverschiebung nur bei klarer Verantwortlichkeit.
3. Nach jedem ausgelagerten Block:
   - `python -m py_compile ...`
   - kurzer Importtest
   - danach erst naechster Block
4. `MCM_Brain_Modell.py` wird schrittweise verkleinert.
5. `debug/` bleibt Datenordner, kein Codeordner.
6. Runtime-Bruecken duerfen vorerst im Brain bleiben, solange sie viele Bot-Seiteneffekte besitzen.

---

# Naechste sinnvolle Aufraeumreihenfolge

1. Root-Dateien sortieren und Rollen festlegen:
   - `bot.py`: Hauptbot und Runtime-Orchestrierung
   - `MCM_Brain_Modell.py`: Brain-Runtime-Bruecke
   - `MCM_KI_Modell.py`: niedriges MCM-Feldmodell
   - `trade_stats.py`: Statistik und Ergebnislernen
   - `config.py`: zentrale Konfiguration
2. Runtime-Funktionen aus `MCM_Brain_Modell.py` pruefen:
   - `_compute_runtime_entry_result`
   - `_compute_runtime_result`
   - `_apply_runtime_result`
   - Snapshot-/Episode-Funktionen
3. `trade_stats.py` spaeter in Statistik, Outcome-Lernen und Debug-Auswertung trennen.
4. Root-Kompatibilitaetsdateien nur entfernen, wenn alle Imports umgestellt sind.
5. Danach erst groessere Ordnerbewegungen.

Prioritaet:
Erst stabile Modulgrenzen, dann Dateiverschiebung. Eine schoene Ordnerstruktur
ist weniger wert als ein lauffaehiger DIO mit klaren Verantwortlichkeiten.

---

# Restlandkarte `MCM_Brain_Modell.py`

Diese Karte dient als Leitlinie fuer die naechsten Auslagerungen.

## Sicherere Auslagerungskandidaten

- Fabrik-/Adapterlogik: reine Objekt-Erzeugung oder Kompatibilitaetsfassaden.
- Snapshot-/Visualisierungslogik: Feldpunkte, Topologie, GUI-Zubringer,
  Debug-Bundles.
- Runtime-Orchestrierung: Tick, Advance, Commit, Refresh, sofern Brain-Formeln
  per Callback injiziert bleiben.

## Vorsichtig behandeln

- Active-Context und Nervensystem-Modulation: wirkt direkt auf Wahrnehmung,
  Reaktionsdruck und innere Kopplung.
- Inner-Pattern-Identity: verbindet Feldtopologie, Wahrnehmung und
  Wiedererkennung.
- Experience-Space: hier entsteht Erfahrungsorganisation, Episodenverdichtung
  und Rueckkopplung.
- Signature-/Cluster-Memory: traegt Kontext, Aehnlichkeit, Stabilitaet,
  Fragilitaet und Ergebnisrueckbindung.
- Felt-/Outcome-Decomposition: sitzt an der Grenze zwischen Handlung,
  Konsequenz und MCM-Feld-Reaktion.

## Arbeitsregel fuer weitere Schnitte

Mechaniktragende Bereiche werden nur verschoben, wenn die Zielgrenze klar ist:
Eingaben, Ausgaben, Bot-State-Schreibpunkte und Rueckkopplung muessen vorher
benannt sein. Keine neue Regel, keine neue Hemmung, keine neue Gewichtung nur
durch Refactoring.

---

# Runtime-Bruecken, die schrittweise wandern

`build_strategic_window_state` liegt jetzt in `core/strategic_window.py`.
Die Funktion verbindet weiterhin mehrere Schichten:

- rueckblickende Bereichswahrnehmung
- Form-/Memory-Resonanz
- Meta-Regulation
- Trade-Plan-Motorik
- Bot-State fuer Debug und Folgeentscheidungen

Die Bruecke hat keine direkten Bot-Schreibpunkte und konnte deshalb als
reiner Besitzerwechsel ausgelagert werden. Lauffaehigkeit bleibt Vorrang vor
weiterer Dateischoenheit.

Bereits ausgelagert:

- `memory/memory_state.py`
  - Bot-Memory-State laden, erfassen und speichern
  - Bot-spezifischen Save-Wrapper halten

- `bot_engine/execution_outcomes.py`
  - Pending-Fill, Non-Action und Entry-Attempt abschliessen
  - Position-Cancel/-Resolution abschliessen
  - bestehende Stats-/Memory-/Episode-Schreibpunkte halten

- `bot_engine/execution_paths.py`
  - Runtime-Ausfuehrungspfade sortieren
  - Payload an Position-/Pending-/Entry-Handler weiterreichen

- `bot_engine/runtime_processing.py`
  - Runtime-Perception-Packet komponieren
  - Runtime mit resolved Market-Packet voranbringen
  - Market-/Runtime-Packet-Verarbeitung finalisieren

- `bot_engine/market_perception.py`
  - Market-Perception-Packets bauen
  - Candle-/Tension-/Visual-/Structure-Packets bilden
  - aeussere Temporal-Perception-Bruecke halten

- `bot_engine/feed_runtime.py`
  - Runtime-Thread-Loop abarbeiten
  - Feed-Fenster konsumieren
  - Market-Packet-Followup ausloesen

- `bot_engine/runtime_timing.py`
  - dynamische Runtime-Last berechnen
  - Idle-Schlafzeit bestimmen
  - Idle-/Followup-Zyklen bestimmen

- `bot_engine/action_context.py`
  - Runtime-Action-Fenster aufloesen
  - Runtime-Action-Payload normalisieren
  - Runtime-Execution-Payload bauen
  - Runtime-Action-Cycle vorbereiten
  - Action-Kontext vorbereiten
  - Timestamp/Position-State anwenden

- `bot_engine/visual_cortex_protocol.py`
  - Visual-Cortex-Diagnose verdichten
  - Visual-Cortex-Protokoll schreiben

- `bot_engine/idle_thinking_protocol.py`
  - Idle-Thinking-Diagnose verdichten
  - Idle-Protokoll schreiben
  - Idle-Protokollfehler melden

- `bot_engine/market_packets.py`
  - Marktfenster normalisieren
  - externes Marktstate-Packet bauen
  - Runtime-Market-Packet bauen
  - Live-Market-Packet-Key ableiten

- `core/runtime_entry.py`
  - Review-/Hypothesen-Feedback in Meta-Regulation
  - Strategic-Window-Werte in Meta-Regulation
  - aktive MCM-Kontaktwahrnehmung in Meta-Regulation
  - Bot-State-Schreibpunkte des Runtime-Entry-Aufbaus
  - Reject-/Nicht-Handlungs-Protokolle fuer Runtime-Entry
  - Trade-Plan-Synchronisierung fuer Entry-Choice
  - virtueller Beobachtungsplan
  - `no-plan` Ergebnisstruktur
  - grosser Entry-Trade-Result-Aufbau
  - finale Ergebnisprotokollierung
  - Runtime-Feldmetriken
  - externe Runtime-Wahrnehmung
  - Welt-/Innenfeld-/Perception-/Processing-Stack
  - Erwartungsdruck-/Felt-/Formsprache-Stack
  - Zeit-/Signatur-/Aktive-Kontextspur-Stack
  - Thought-/Meta-Regulation-Stack
  - Review-/Strategic-/MCM-Kontakt-Regulation-Stack

Stand nach Refactoring Phase 4bc:

- Modulare Auslagerung: ca. 100 % der Runtime-Entry-Kleinschnitte
- Bot-Orchestrierung: Market-Packet-Helfer aus `bot.py` ausgelagert
- Bot-Orchestrierung: Market-Perception-Aufbau aus `bot.py` ausgelagert
- Bot-Orchestrierung: Runtime-Processing aus `bot.py` ausgelagert
- Bot-Orchestrierung: Execution-Path-Wrapper aus `bot.py` ausgelagert
- Bot-Orchestrierung: Execution-Outcome-Helfer aus `bot.py` ausgelagert
- Bot-Orchestrierung: Runtime-Action-Context aus `bot.py` ausgelagert
- Bot-Orchestrierung: Runtime-Taktung aus `bot.py` ausgelagert
- Bot-Orchestrierung: Feed-/Runtime-Loop aus `bot.py` ausgelagert
- Debug-Orchestrierung: Idle-Thinking-Protokoll aus `bot.py` ausgelagert
- Debug-Orchestrierung: Visual-Cortex-Protokoll aus `bot.py` ausgelagert
- Naechster Restblock:
  - `build_strategic_window_state` als eigene Strategic-Window-Bruecke pruefen
  - Runtime-Entry-Orchestrator ggf. weiter aus dem Brain herausloesen

---

# Runtime-Orchestrierung

Der Bot-Thread ist Orchestrierung, nicht MCM-Kern. Er darf technische
Sicherungen besitzen, solange diese keine Entscheidung erzwingen.

Aktuelle technische Sicherungen:

- Stop-Timeout fuer Runtime-Thread
- Queue-Idle-Timeout fuer Debug-/Smoke-Laeufe
- Watchdog-Protokoll fuer haengende Thread-/Queue-Zustaende

Diese Sicherungen veraendern keine neuronale Entscheidung. Sie verhindern nur,
dass ein technischer Lauf ohne Diagnose stehen bleibt.
