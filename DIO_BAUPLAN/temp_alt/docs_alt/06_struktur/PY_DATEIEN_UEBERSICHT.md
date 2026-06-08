# Python-Dateien Übersicht

Diese Datei beschreibt kurz, wofür die aktiven `.py`-Dateien im Projekt stehen.
Sie ist eine Orientierungshilfe, keine Detaildokumentation der gesamten Mechanik.

Aktueller Architekturstand:

- DIO liest keinen einzelnen Kerzenwert als Entry-Signal.
- Die Aussenwelt laeuft als Kerzenstrom weiter; DIO verarbeitet parallel im
  eigenen Runtime-Thread.
- Kerzen erscheinen als sensorische Ereignisse und bilden Teilformen,
  Formfolgen, MCM-Spuren und emergente Mustervarianz.
- Entry-Naehe soll aus einer gereiften These entstehen:
  `Kerzenstrom -> Teilform -> Form/MCM-Resonanz -> Variantenraum -> These -> Reife -> moeglicher Entry`.
- `trading/trade_plan.py` nutzt den Impuls nicht mehr als konkreten
  Entry-Anker. Impuls bleibt Diagnose/Wahrnehmungsdruck; Entry-Naehe entsteht
  aus gereifter Bereichs-/MCM-/Hypothesen-These.

## Root

| Datei | Zweck / Funktion |
| --- | --- |
| `_gui.py` | Haupt-GUI für DIO mit Chart, PnL, Trade-Stats, Candle-State und Backtest-Fortschritt. |
| `_neuronen_gui.py` | Visualisierung der MCM-Neuronen-/Feldaktivität. |
| `api.py` | API-nahe Hilfs- oder Startschicht für externe Anbindung. |
| `bot.py` | Zentrale Bot-Klasse; verbindet Runtime, Feed, Entry, Position, Memory, Debug und Bot-Engine-Module. |
| `config.py` | Zentrale Konfiguration für Modus, Datenquelle, MCM, Debug, Zeitfenster, Risiko und Laufprofile. |
| `MCM_Brain_Modell.py` | Haupt-Brain-Brücke; bündelt MCM-Runtime, Brain-Step, Outcome-Stimulus und ältere Kompatibilitätsfunktionen. |
| `runner.py` | Startpunkt für Backtest, Smoke-Test und Live-Modus. |
| `workspace.py` | Workspace-Hilfen für Live-/CSV-Datenablage. |

## Core

| Datei | Zweck / Funktion |
| --- | --- |
| `core/__init__.py` | Paketmarker und kurzer Core-Kontext. |
| `core/active_context.py` | Baut aktive Kontextspuren aus aktuellem Wahrnehmungs-/Erfahrungszustand. |
| `core/brain_factory.py` | Erzeugt Brain-Grundstruktur und verbindet Core-Komponenten. |
| `core/decision_regulation.py` | Meta-Regulation, Pre-Action-Zustände, innere Zustimmung, Reife, Vorsicht und Handlungsnähe. |
| `core/experience_space.py` | Erfahrungsraum und Rückführung von Outcome-/Kontextinformationen. |
| `core/felt_state.py` | Übersetzt Feld-/Wahrnehmungszustände in gefühlte innere Lage. |
| `core/form_language.py` | DIO-Formsprache; verdichtet Form-/MCM-Zustände in eigene Syntax. |
| `core/form_symbol_orchestration.py` | Orchestriert Formsymbol-Zustand, Entwicklung und Outcome-Rückführung. |
| `core/hypothesis_learning.py` | Reale Form/MCM-Familien als Anker; Hypothesen als `thought_trace`. Lernschicht für Hypothesen, beobachtete Varianten und deren spätere Tragfähigkeit. |
| `core/inner_context.py` | Innerer Kontext, neuronale Kontextcluster und Memory-Resonanz im Feld. |
| `core/inner_pattern.py` | Innere Musterlagen, Pattern-Support, Fragilität und Wiederkehr. |
| `core/mcm_field.py` | MCM-Feld, Neuronenlogik, Feldzustände und topologische MCM-Mechanik. |
| `core/mcm_model.py` | Modellnahe MCM-Hilfsstruktur und Basislogik. |
| `core/neurochemistry.py` | Neurochemische Zuordnung wie Stabilität, Last, Aktivierung, Druck und Regeneration. |
| `core/perception.py` | Wahrnehmungsstack aus Außenwelt, Innenfeld, visueller Form, Denken und MCM-Kopplung. |
| `core/possibility_field.py` | Variantenraum für LONG, SHORT, WAIT, REPLAN aus Form, MCM, Zeit, Doppler und Memory. |
| `core/review_feedback.py` | Rückblick-/Feedback-Schicht für Entscheidungen, Hypothesen und spätere Bewertung. |
| `core/runtime.py` | MCM-Runtime-Klasse; verarbeitet Ticks und Advance-Schritte. |
| `core/runtime_bridge.py` | Brücke zwischen Bot und MCM-Runtime. |
| `core/runtime_commit.py` | Schreibt Runtime-Ergebnisse zurück in Bot-State und Debug-/Memory-Kontext. |
| `core/runtime_entry.py` | Baut Runtime-Entry-State, Trade-Result, Rejection-Protokolle und Entry-Synchronisierung. |
| `core/runtime_field_state.py` | Snapshot- und Zustandsableitung aus dem MCM-Feld. |
| `core/runtime_snapshot.py` | Runtime-Snapshot für Diagnose und Übergabe an andere Schichten. |
| `core/runtime_tendency.py` | Leitet Handlungstendenz wie hold, observe, replan oder act aus Runtime-Zustand ab. |
| `core/strategic_window.py` | Strategische Rückblick-/Bereichswahrnehmung für mögliche Entry-Thesen. |
| `core/temporal_perception.py` | Zeitwahrnehmung, Nachhall, Vorhall, Raumzeit-Fit und zeitliche Tiefe. |
| `core/thought_memory.py` | Innere Gedankenkeime, Gedankenfamilien, Reife, Trust und Thought-Memory-Logik. |

## Bot-Engine

| Datei | Zweck / Funktion |
| --- | --- |
| `bot_engine/__init__.py` | Paketmarker für Bot-Engine-Module. |
| `bot_engine/action_context.py` | Baut und normalisiert Action-Kontext für Runtime, Entry, Pending und Position. |
| `bot_engine/active_position.py` | Verarbeitung offener Positionen inklusive Exit-, Update- und Outcome-Pfad. |
| `bot_engine/entry_attempt.py` | Behandelt Entry-Versuche, Value-Gate, Order-Platzierung und Abbruchpfade. |
| `bot_engine/entry_attempt_context.py` | Baut Kontextdaten für Entry-Attempts und deren spätere Auswertung. |
| `bot_engine/execution_outcomes.py` | Finalisiert Positionen, Pending-Fills, Cancels, Timeouts und Outcome-Stimuli. |
| `bot_engine/execution_paths.py` | Verzweigt Runtime-Pfade: Position, Pending, Entry oder Decision. |
| `bot_engine/exit_candidate_observe.py` | Beobachtet mögliche gereifte Exit-Kandidaten ohne zwingend aktiv zu schließen. |
| `bot_engine/exit_engine.py` | Technische Exit-Engine für TP/SL, aktive Positionsauflösung und Exit-Status. |
| `bot_engine/feed_runtime.py` | Feed-/Runtime-Schleife für Marktdatenpakete, Fenster und Follow-up. |
| `bot_engine/idle_thinking_protocol.py` | Live-/Idle-Denkzeitprotokoll und Phasenauflösung. |
| `bot_engine/live_recovery.py` | Wiederherstellung von Live-Status, Positionen und Orders beim Start. |
| `bot_engine/market_packets.py` | Normalisiert und baut Market-Packets, Live-Dedupe und Runtime-Payloads. |
| `bot_engine/market_perception.py` | Baut Candle-, Visual-, Structure-, Temporal- und Perception-Pakete. |
| `bot_engine/matured_exit.py` | Ableitung gereifter Exit-Signale und Schutz-/Giveback-Interpretation. |
| `bot_engine/mcm_core_engine.py` | Kernübersetzung von Marktdaten in Spannung, visuelle Marktform und MCM-Stimulus. |
| `bot_engine/pending_entry.py` | Verwaltung wartender Pending-Entries, Fill-Erkennung, Timeout und Handoff. |
| `bot_engine/position_intervention.py` | Diagnose von Positionslast, Exit-Druck und Interventionsfähigkeit. |
| `bot_engine/regulation_snapshot.py` | Baut Snapshots und Deltas der Regulationszustände. |
| `bot_engine/restart_recovery.py` | Wendet gespeicherte Restart-/Recovery-Zustände an. |
| `bot_engine/runtime_followup.py` | Runtime-Follow-up, Memory-Flush, Idle-Schritte und Nachbearbeitung. |
| `bot_engine/runtime_processing.py` | Verarbeitung von Market-Packets durch Runtime und Seed-/Advance-Pfade. |
| `bot_engine/runtime_thread.py` | Separater Runtime-Thread, Queue, Start/Stop/Idle-Handling. |
| `bot_engine/runtime_timing.py` | Zeit-/Timing-Hilfen für Runtime und Taktung. |
| `bot_engine/state_initialization.py` | Initialisiert Bot-State, Runtime-Variablen, Memory-Defaults und Debug-Pfade. |
| `bot_engine/strukture_engine.py` | Struktur-Engine für Marktstruktur-Auswertung und ältere Strukturpfade. |
| `bot_engine/target_expectation.py` | Zielerwartung, TP-Erreichbarkeit und Erwartungsdruck. |
| `bot_engine/visual_cortex_protocol.py` | Protokolliert visuelle Cortex-/Formsehen-Zustände. |
| `bot_engine/visualization_snapshots.py` | Baut und schreibt Visualisierungs-Snapshots für GUI/Debug. |
| `bot_engine/world_motion_afterimage.py` | Bewegte-Welt-Nachhall, Doppler, Vorhall und sensorische Kerzenstromspur. |

## Bot-Gates

| Datei | Zweck / Funktion |
| --- | --- |
| `bot_gates/entry_decision.py` | Entry-Gate: prüft Runtime-Tendenz, innere Zustimmung, Hypothesenreife und Trade-Geometrie. |
| `bot_gates/trade_value_gate.py` | Ökonomisches Value-Gate für Entry/SL/TP, RR, Mindestbewegung und Risikoabstand. |

## Trading

| Datei | Zweck / Funktion |
| --- | --- |
| `trading/__init__.py` | Paketmarker für Trading-Module. |
| `trading/backtest_runtime.py` | Backtest-nahe Runtime-Hilfen und Ausführungskontext. |
| `trading/csv_feed.py` | CSV-Feed für OHLCV-Daten und Backtest-Fenster. |
| `trading/exchange_data.py` | Börsen-/Exchange-Daten, Symbolauflösung, Kontowert und OHLCV-Abruf. |
| `trading/live_runtime.py` | Live-Runtime-nahe Hilfen für Börsenbetrieb. |
| `trading/order_api_helpers.py` | Hilfsfunktionen für Order-API, Parameter und Exchange-Operationen. |
| `trading/order_logic.py` | Order-Erstellung, Cancel, Kontext, Monitor und Live-Order-Pfade. |
| `trading/trade_plan.py` | Berechnet Entry, SL, TP und RR aus Brain-Zustand, strategischem Fenster und MCM-Kontext. Entry-Preise entstehen jetzt primaer aus gereifter Form-/MCM-/Hypothesen-These; Impuls bleibt Wahrnehmungsdruck/Diagnose. |
| `trading/trade_stats.py` | Trade-Statistik, Equity, Attempts, Outcomes, Hypothesenbewertung und Debug-Ausgaben. |

## Memory

| Datei | Zweck / Funktion |
| --- | --- |
| `memory/__init__.py` | Paketmarker für Memory-Module. |
| `memory/form_symbol_memory.py` | Persistenter Speicher für DIOs Formsprache und Formsymbol-Familien. |
| `memory/memory_state.py` | Weltlicher Bot-Memory-State, Laden, Speichern und Flush-Logik. |
| `memory/thought_memory_store.py` | Persistenter Speicher für innere Gedankenkeime und Thought-Familien. |

## Debug-Tools

| Datei | Zweck / Funktion |
| --- | --- |
| `debug_tools/__init__.py` | Paketmarker für Debug-Module. |
| `debug_tools/debug_reader.py` | Liest und analysiert Debug-Ausgaben. |
| `debug_tools/field_snapshots.py` | Schreibt Feld-/Topologie-Snapshots für spätere Analyse. |
| `debug_tools/protocols.py` | Zentrale Debug-Protokolle für MCM, Memory, Thought, Field, Entry und Neurochemie. |
| `debug_tools/visualization.py` | Visualisierungsdaten für GUI und Analyse. |
| `debug_tools/writers.py` | Debug-Schreiblogik, Buffering, Pfade, Laufordner und File-Write-Profiling. |

## Data Builder

| Datei | Zweck / Funktion |
| --- | --- |
| `data_builder/binance_ohlcv_builder.py` | Erstellt OHLCV-CSV-Daten aus Binance-Datenquellen. |

## Alte GUIs

| Datei | Zweck / Funktion |
| --- | --- |
| `old_guis/_gui_mcm_inner_space.py` | Alte GUI-Variante für inneren MCM-Raum. |
| `old_guis/_gui_mcm_neuron_field.py` | Alte GUI-Variante für MCM-Neuronenfeld. |
| `old_guis/_gui_mcm_neuron_field_gpu.py` | Alte GPU-nahe GUI-Variante für Neuronenfeld-Visualisierung. |
| `old_guis/_gui_mcm_perception.py` | Alte GUI-Variante für Wahrnehmungs-/Perception-Ansicht. |
| `old_guis/_gui_older.py` | Ältere allgemeine GUI-Version. |
| `old_guis/_simple_gui.py` | Einfache alte GUI-Variante. |

## Tests

| Datei | Zweck / Funktion |
| --- | --- |
| `tests/test_bot_gate_funktions.py` | Prüft Entry-/Gate-Verhalten und Bot-Gate-Funktionen. |
| `tests/test_bot_live_cancel_persistence.py` | Prüft Persistenz bei Live-Cancel-Pfaden. |
| `tests/test_bot_outcome_sync.py` | Prüft Synchronisierung von Outcome-Daten im Bot. |
| `tests/test_bot_pending_fill_persistence.py` | Prüft Persistenz bei Pending-Fill-Handoff. |
| `tests/test_bot_timeout_outcome_persistence.py` | Prüft Timeout-Outcomes und deren Speicherung. |
| `tests/test_decision_regulation.py` | Prüft Entscheidungs-/Regulationslogik. |
| `tests/test_form_mcm_syntax.py` | Prüft Formsprache und MCM-Syntax-Verknüpfung. |
| `tests/test_mcm_brain_learning_timing.py` | Prüft Lern- und Timing-Verhalten des MCM-Brains. |
| `tests/test_mcm_core_engine.py` | Prüft Kernübersetzung der MCM-Core-Engine. |
| `tests/test_mcm_runtime_integration.py` | Prüft Integration der MCM-Runtime. |
| `tests/test_memory_state_persistence.py` | Prüft Laden/Speichern des Memory-State. |
| `tests/test_review_feedback.py` | Prüft Review-/Feedback-Schichten. |
| `tests/test_runtime_regulation_mapping.py` | Prüft Mapping von Runtime-Zuständen in Regulation. |
| `tests/test_trade_stats_outcome_decomposition.py` | Prüft Trade-Stats und Outcome-Decomposition. |
