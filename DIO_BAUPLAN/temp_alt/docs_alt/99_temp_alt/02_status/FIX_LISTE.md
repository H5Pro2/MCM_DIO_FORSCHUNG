# FIX_LISTE

Hinweis zum aktiven Bauplan:

Diese Datei bleibt als alte Fixlisten-Referenz erhalten. Die aktive Arbeitslogik
liegt jetzt in:

- `ARBEITSSPUR.md`
- `../../DIO_2/konstruktion/12_ARBEITSSPUR.md`

Neue Punkte sollen dort knapp als Arbeitsrichtung geführt werden, nicht mehr als
überladene Fixliste.

---

- [x] DIO-Schichtmodell als Rueckbau-Referenz festhalten.
  Datei:
  - `docs/07_konstruktion/DIO_SCHICHTMODELL_NEUAUFBAU.md`
  Zielordnung:
  - Welt
  - Sehen
  - MCM-Feld
  - Memory
  - Thought
  - Realitaetspruefung
  - Handlung
  - Konsequenz
  Umsetzung begonnen:
  - `trading/trade_plan.py` behandelt Hypothesen nicht mehr als
    Entry-Anker.
  - `hypothesis_action_support` hebt keine Motorik/Entry-Reife mehr an.
  - `hypothesis_observation_pressure` bleibt als vorsichtige Feldwirkung
    erhalten.
  - Entry-Modi gehen wieder auf `area_contact_intention` und
    `area_contact_entry` zurueck.
  Naechste Pruefung:
  - weniger `hypothesis_area_entry`
  - mehr reale `area_contact_*`-Entries
  - offene Hypothesen wirken als Deutung/Abstand, nicht als Handlung.

- [x] Debug-Diät für normale Backtests aktivieren.
  Ergebnis:
  - `DEBUG_OUTPUT_PROFILE` steht standardmäßig auf `LEAN_BACKTEST`.
  - `LEAN_BACKTEST` schreibt keine schweren `outcome_records.jsonl`-Rohdaten.
  - Attempt-Rohrecords, Neuro-Transition, Position-Intervention,
    Exit-Candidate-Observe, Form-Symbol- und Visual-Cortex-Protokolle sind im
    Standardlauf aus.
  - `mcm_field_decision_protocol.csv` und `mcm_thought_digest_protocol.csv`
    bleiben nur stark gesampelt aktiv.
  - Zustandswechsel erzeugen im schlanken Lauf keine Zusatzzeilen mehr
    (`MCM_PROTOCOL_CHANGE_BURST_DEBUG = False`).
  - GUI/KPI-Daten bleiben erhalten.
  Zweck:
  - weniger Datei- und Debuglast
  - klarere Trennung zwischen normalem Backtest und Forschungslauf
  - Mechanik bleibt unverändert; nur die äußere Protokollierung wird dosiert.
  Forschungsmodus:
  - Für tiefe Analyse `DEBUG_OUTPUT_PROFILE = "RESEARCH_DEBUG"` setzen.

- [ ] Entmechanisierung beginnen: Core und starre Logik gezielt rueckbauen.
  Referenz:
  - `docs/07_konstruktion/ENTMECHANISIERUNG_PLAN.md`
  - `docs/07_konstruktion/ENTMECHANISIERUNG_ABGLEICH.md`
  Fokus:
  - Core-Chartdaten auf energetische Basisspur reduzieren.
  - Harte Gates in Sicherheitsinvarianten, Feldmodulation und mechanische
    Reste klassifizieren.
  - Mechanische Wenn-Dann-Logik entfernen oder in weiche MCM-Feldwirkung
    ueberfuehren.
  - Hypothesen als Gedankenspuren an realen Formankern halten.
  Pruefung:
  - weniger `no_mature_entry_thesis` als pauschaler Restzustand
  - weniger Gate-getriebene Nicht-Handlung
  - mehr nachvollziehbare Feldtendenz aus Energie, Kohaerenz, Asymmetrie,
    Regime, Formwiederkehr und Konsequenz
  Aktueller Core-Schritt:
  - `bot_engine/mcm_core_engine.py` trennt Kernspur und abgeleitete Deutung.
  - Visual-Sehen nach `core/visual_perception.py` ausgelagert.
  - Sensory-Reizlage nach `core/sensory_reality.py` ausgelagert.
  - Alte Visual-Felder bleiben kompatibel erhalten.
  - `core/perception.py` liest jetzt zuerst Trace-Zustaende und fuehrt sie im
    Output mit.
  - `uncertainty_score`, `novelty_score`, `signal_quality` und
    `observe_priority` sind in Trace- und Interpretationsanteile zerlegt.
  Naechster Schritt:
  - Downstream-Nutzung dieser Score-Namen pruefen.
  - Besonders `core/decision_regulation.py` darf diese Werte nicht mehr als
    harte Handlungsnaehe behandeln.

- [ ] Gate-Begriff bereinigen: nur Value-Gate bleibt echtes Gate.
  Architekturregel:
  - keine harten Gates fuer innere Zustaende
  - Reife, Vertrauen, Vorsicht, Ueberlastung und Unsicherheit wirken als
    Feldmodulation
  - einziges echtes Gate: oekonomische Value-Pruefung mit valider
    Preis-/Risiko-/Order-Geometrie
  Umsetzung begonnen:
  - `core/decision_regulation.py`
  - `_build_pre_action_decision_state()` fuehrt innere `allow_block`-Pfade auf
    Feldmodulation zurueck.
  - `former_allow_block` bleibt diagnostisch sichtbar.
  - `bot_gates/entry_decision.py`
  - `_resolve_inner_action_consent()` blockiert nicht mehr hart, sondern
    markiert `inner_action_would_have_declined`.
  - `runtime_allow_plan_false` ist Meta-Diagnose, kein harter Return mehr.
  Naechster Schritt:
  - Begriffe wie `inner_action_declined`, `execution_blocked` und
    `signature_block` fachlich pruefen und ggf. in Feld-/Diagnosebegriffe
    ueberfuehren.

- [ ] Naechsten Lauf auf saubere Realitaetstrennung pruefen.
  Anlass:
  - Hypothesen duerfen keine eigene Realitaet und keine eigene
    Vertrauensfamilie bilden.
  - Der Speicheranker muss die reale Form-/MCM-Lage bleiben.
  - Entry-Bereich, gedachte Fortsetzung und strategische Entry-Lage sind nur
    `thought_trace` an diesem realen Anker.
  Pruefung:
  - `dominant_hypothesis_trust_key` soll auf reale Formanker zeigen
    (`fs_*`, `fc_*`, semantisches Formprofil), nicht auf `thesis:*`.
  - `hypothesis_trust_families` sollen keine `thesis:*`, `area:*` oder
    `area_mode:*`-Familien mehr erzeugen.
  - `recent_observation_learning` darf weiter Entry-/Area-Kontext zeigen, aber
    als Gedankenspur, nicht als Realitaetsanker.

- [x] Alte Area-These-Familien verworfen.
  Ergebnis:
  - Area-/Entry-Metadaten bleiben erhalten, aber nur als `thought_trace`.
  - Sie bilden keine eigene Vertrauensfamilie mehr.
  - Vertrauen reift wieder am realen Form-/MCM-Anker.

- [ ] Echte Backtest-Weltzeit-Entkopplung pruefen.
  Umsetzung:
  - `BACKTEST_WAIT_FOR_RUNTIME_IDLE = False`
  - `RUNTIME_MAX_QUEUE_SIZE = 3`
  - Backtest nutzt keinen Runtime-Thread und keine Runtime-Queue mehr.
  - Backtest verarbeitet jedes Fenster direkt im Offline-Replay.
  - Backtest wartet nicht mehr pro Kerze auf DIO-Thread-Idle.
  - Backtest schlaeft nicht mehr real pro CSV-Zeile.
  - Queue-Drops betreffen den Backtest nicht mehr, sondern nur Live/Async.
  Letzter Befund:
  - `world_published_ticks = 34061`
  - `world_missed_ticks = 34050` nach zu hartem Feed ohne Backpressure
  - `cognitive_lag_pressure = 1.0`
  - Ursache war teilweise eine Zeitueberschneidung:
    `WORLD_TIME_SECONDS` wurde als fachliche Weltzeit und als echtes
    Backtest-Feed-Sleep genutzt.
  - Backpressure war als Zwischenfix ebenfalls nicht sauber, weil es die
    Backtest-Aussenwelt wieder an die Runtime-Queue gekoppelt hat.
  Messpunkte:
  - `world_missed_ticks`
  - `cognitive_lag_pressure`
  - Queue-Verhalten
  - Laufzeit
  - Tradeanzahl
  - ob DIO weniger Muster endlos durchdenkt

- [x] Zeitparameter fachlich vereinheitlichen.
  Umsetzung:
  - aktive Config hat nur noch `WORLD_TIME_SECONDS`
  - aktive Config hat nur noch `GLOBAL_COGNITIVE_REACTION_SECONDS`
  - `MCM_THOUGHT_MEMORY_UPDATE_MIN_TICK_GAP` bleibt als Weltzeit-Tickfenster
  - alte Loop-/Replay-/MCM-Doppelwerte entfernt
  - Backtest nutzt CSV-Timestamps als Marktzeit und schlaeft nicht real pro
    Zeile
  - Live nutzt den Timeframe als Weltzeit
  Pruefung:
  - Compile OK
  - 38 Tests OK

- [ ] Weltzeit-/Denkzeitparameter im naechsten Lauf beobachten.
  Werte:
  - `WORLD_TIME_SECONDS = 0.001`
  - `GLOBAL_COGNITIVE_REACTION_SECONDS = 0.000001`
  - `MCM_THOUGHT_MEMORY_UPDATE_MIN_TICK_GAP = 8`
  Fokus:
  - ob `thought_memory_update` seltener wird
  - ob deferred Thoughts steigen
  - ob die Laufzeit sinkt
  - ob die Thought-Memory-Bildung weiterhin tragende Familien erzeugt

- [ ] Entkopplung Weltzeit/Denkzeit im naechsten Lauf pruefen.
  Umsetzung:
  - Thought-Memory-Update hat jetzt ein weiches Weltzeitbudget.
  - Nicht jeder Thought-Seed wird sofort persistent verdichtet.
  - Deferred Thoughts bleiben sichtbar, aber werden nicht jedes Mal in den
    Speicher gedrueckt.
  Messpunkte:
  - Anzahl `thought_memory_update`
  - `thought_memory_deferred_count`
  - Laufzeitgefuehl
  - Thought-Memory-Groesse
  - ob Muster nicht mehr tausendfach gleich durchdacht werden
  - ob DIO trotzdem lernt und tragende Gedanken speichert

- [ ] `_update_thought_memory()` im naechsten Lauf auswerten.
  Umsetzung:
  - direkter Profiling-Eintrag `thought_memory_update`
  - Ausgabe in `performance/mcm_file_write_profile.csv`
  Auswertung:
  - Anzahl Aufrufe
  - Durchschnittsdauer
  - Maximaldauer
  - ob `normalize_trim` auftritt
  - Seeds/Families/Form-MCM-Families pro Update
  Ziel:
  - klaeren, ob Denklast aus Thought-Update selbst oder aus Persistenz kommt

- [ ] Naechsten Lauf auf reduzierte Thought-Memory-Update-Last pruefen.
  Anlass:
  - Denklast entsteht nicht nur durch Datei-Schreiben.
  - Thought-Memory wurde zwar nur einmal geladen, aber pro Update wurden
    grosse Dicts kopiert und Summary-Zaehler voll neu berechnet.
  Umsetzung:
  - Thought-Memory wird im laufenden Speicher direkt fortgeschrieben.
  - keine Vollkopien pro Gedankenkeim.
  - Summary-Zaehler werden inkrementell aktualisiert.
  Fokus:
  - Laufzeitgefuehl
  - Thought-Memory-Wachstum
  - `mcm_file_write_profile.csv`
  - ob DIO weiterhin Gedankenfamilien sinnvoll bildet

- [ ] Naechsten Lauf auf Memory-/Kognitionslast pruefen.
  Anlass:
  - 120 Neuronen allein haben nicht ausreichend beschleunigt.
  - Lauf 343 zeigte grosse Thought-Memory-Schreibvorgaenge.
  Umsetzung vor dem Lauf:
  - Thought-Memory speichert nur noch alle `256` Updates.
  - Form-Symbol-Memory speichert nur noch alle `256` Updates.
  - beide Speicher schreiben kompakteres JSON.
  - beide periodischen Speicher respektieren den Memory-Cooldown.
  Fokus:
  - `performance/mcm_file_write_profile.csv`
  - Groesse von `bot_memory/mcm_thought_memory.json`
  - Groesse von `bot_memory/form_symbol_memory.json`
  - Laufzeitgefuehl
  - ob Thought-Memory weiter sinnvoll waechst

- [ ] Lauf mit `MCM_FIELD_NEURON = 120` gegen Lauf 340 auswerten.
  Anlass:
  - MCM-Field ist Hauptlaufzeitblock.
  - Neuronenzahl wurde von `230` auf `120` reduziert.
  Ziel:
  - pruefen, ob Laufzeit sinkt
  - pruefen, ob DIO ruhiger oder blind/zu grob wird
  - Tradeanzahl, PnL-Verlauf und Profiling vergleichen
  Fokus:
  - `mcm_field.step.neuron_loop`
  - `mcm_field.step.activity_diffusion`
  - `step_mcm_brain.primary_field_step`
  - `mcm_thought_landkarte.txt`

- [x] Leichtes Profiling im aktiven Core-Debug einschalten.
  Ziel:
  - naechsten Lauf messbar machen
  - keine Tradingmechanik veraendern
  - Debug-I/O, Memory und Regulation trennen koennen
  Umsetzung:
  - `DIO_CORE_DEBUG`:
    - `MCM_RUNTIME_PROFILE_DEBUG = True`
    - `MCM_RUNTIME_PROFILE_EVERY_N = 25`
    - `MCM_FILE_WRITE_PROFILE_DEBUG = True`
    - `MCM_FILE_WRITE_PROFILE_EVERY_N = 25`
  Pruefung:
  - Compile OK
  - kompletter Testlauf: 38 Tests OK

- [x] Naechsten Profiling-Lauf auswerten.
  Dateien:
  - `performance/mcm_profile.csv`
  - `performance/mcm_file_write_profile.csv`
  - `core/mcm_field_decision_protocol.csv`
  - `core/mcm_thought_digest_protocol.csv`
  Ziel:
  - Hauptengpass bestimmen:
    - Debug-I/O
    - Thought-Memory
    - Runtime-/Regulation-Stack
    - MCM-Field
  Ergebnis Lauf 340:
  - Hauptengpass ist MCM-Field/Brain-Step, nicht Datei-I/O.
  - groesste Bloecke:
    - `step_mcm_brain.primary_field_step`
    - `mcm_field.step.neuron_loop`
    - `mcm_field.step.activity_diffusion`
    - `step_mcm_brain.snapshot_field_read`
  - `mcm_thought_landkarte.txt` ist mit ca. 28 KB ausreichend reduziert.

- [x] MCM-Field-Schritt technisch entlasten, ohne organische Logik zu aendern.
  Anlass:
  - Profiling Lauf 340 zeigt MCM-Field als Hauptlaufzeitblock.
  Ziel:
  - keine neue Handelsregel
  - keine harte Blockade
  - gleiche Wahrnehmungsmechanik, aber weniger doppelte Arbeit
  Pruefpunkte:
  - doppelte Snapshot-/Cluster-Lesungen vermeiden
  - Neuron-Loop und Diffusion auf wiederholte Berechnungen pruefen
  - Areal-/Nachbarschaftszustaende pro Tick cachen
  - Debug-Protokolle nur nach fertigem Zustand befuellen, nicht waehrend
    jeder inneren Teilbewegung
  Umsetzung:
  - `_apply_activity_diffusion()` nutzt jetzt vorbereitete Arrays fuer
    Zustand, Aktivierung, Kopplung, Kontext, Ueberlastung, Erholung und
    Rezeptivitaet.
  - Nachbarschaftsgewichte werden vektorisiert gebildet.
  - keine Veraenderung der organischen Gewichtungslogik.
  Pruefung:
  - Compile OK
  - 38 Tests OK

- [ ] Naechsten Lauf gegen Lauf 340 messen.
  Fokus:
  - sinkt `mcm_field.step.activity_diffusion`
  - bleibt `step_mcm_brain.primary_field_step` stabil
  - bleiben Tradeanzahl und Zurueckhaltung organisch ruhig
  - keine Rueckkehr zu Mikrotrading

- [x] Laufzeit-Engpass mit Profiling messen.
  Anlass:
  - Lauf 337 zeigt: `mcm_thought_landkarte.txt` ist stark reduziert.
  - Trotzdem bleiben Laufzeit und Core-Debug schwer.
  Befund:
  - `mcm_field_decision_protocol.csv`: ca. 7.0 MB
  - `mcm_thought_digest_protocol.csv`: ca. 4.6 MB
  - `mcm_thought_memory.json`: zuletzt ca. 12.5 MB
  - Regulation weiter belastet:
    - `regulatory_second_order_load` ca. 0.56
    - `hypothesis_trust` ca. 0.018
    - `inner_outer_alignment` ca. 0.185
  Ziel:
  - trennen, ob die Laufzeit hauptsaechlich durch Debug-I/O,
    Thought-Memory-Update oder echte Regulation/Field-Berechnung entsteht.
  Vorgehen:
  - kurzer Profiling-Lauf
  - danach Debug- und Memory-Pfade gezielt entlasten
  - keine Veraenderung an Entry-/Tradingmechanik, solange die Ursache nicht
    gemessen ist.
  Ergebnis:
  - erledigt mit Lauf 340
  - Hauptengpass ist MCM-Field/Brain-Step
  - Debug-I/O und Memory-Schreiben sind messbar, aber nicht dominant

- [x] Thought-Landkarte auf fundamentale Gedanken reduzieren.
  Ziel:
  - nicht jeden Gedanken lesen
  - nur fundamentale Denkumschlaege sichtbar machen
  - Landkarte sehr flach halten
  - normale innere Bewegung im Digest/Memory lassen
  Umsetzung:
  - `MCM_THOUGHT_LANDKARTE_EVERY_N = 120`
  - `MCM_THOUGHT_LANDKARTE_MIN_EVENT = 0.62`
  - neuer interner `fundamental_shift`
  - `act` und `replan` werden nur noch sichtbar, wenn sie wirklich von
    Ereignis, Hypothese, Mismatch oder Denk-Last getragen sind.
  Pruefung:
  - Compile OK
  - kompletter Testlauf: 38 Tests OK

- [ ] Naechsten Lauf auf fundamentale Landkarte pruefen.
  Fokus:
  - Zeilenanzahl von `mcm_thought_landkarte.txt`
  - ob nur noch echte Umschlaege sichtbar sind
  - ob die Datei fuer menschliche Auswertung ausreichend bleibt
  - ob weitere Reduktion auf Abschnitts-Root-Zustaende sinnvoll ist

- [x] Thought-Digest-Debug nach Lauf 334 entlasten.
  Befund:
  - `mcm_thought_digest_protocol.csv` schrieb 7728 Zeilen.
  - Ursache: der Debug-Schluessel enthielt `thought_seed_id`.
  - Da Thought-Seeds fein variieren, wurde fast jeder Tick als neuer
    Digest-Zustand geschrieben.
  Umsetzung:
  - Debug-Schluessel auf groebere Familie/Zustandslage umgestellt:
    - `dio_form_mcm_family_token`
    - Digest-Zustand
    - Reifungsrichtung
    - Open-Hypothesen-Zustand
    - Phase
    - grobe Qualitaets-Buckets
  - `DIO_CORE_DEBUG`: `MCM_THOUGHT_DIGEST_PROTOCOL_EVERY_N` von `10` auf
    `25` gesetzt.
  Wichtig:
  - reine Debug-Entlastung
  - keine Aenderung der Denk-/Entry-/Memory-Mechanik
  Pruefung:
  - Compile OK
  - kompletter Testlauf: 38 Tests OK

- [ ] Naechsten Lauf auf Laufzeit-Engpass pruefen.
  Fokus:
  - sinken Zeilen und MB von `mcm_thought_digest_protocol.csv` deutlich?
  - bleibt `mcm_thought_landkarte.txt` schlank?
  - ist `mcm_field_decision_protocol.csv` danach der Haupt-I/O-Treiber?
  - falls Laufzeit weiter hoch bleibt: Profiling kurz aktivieren oder
    gezielt Memory-Update/JSON-Schreibpfad messen.

- [x] Landkarten-Filter nach Lauf 332 nachschaerfen.
  Befund:
  - `mcm_thought_landkarte.txt` war mit 1563 Zeilen noch zu gespraechig.
  - Ursache: jeder `act`- und `replan`-Wechsel wurde als wichtig behandelt.
  Umsetzung:
  - `act` und `replan` schreiben nur noch bei echter Ereignisstaerke,
    Mismatch, Denk-Last oder Denk-Sparbedarf voll aus.
  - sonst werden sie als Verdichtungsstrecke getragen.
  Pruefung:
  - Compile OK
  - kompletter Testlauf: 38 Tests OK

- [ ] Entry-Freigabe gegen Hypothesenqualitaet pruefen.
  Befund aus Lauf 332:
  - 3 echte Entries, alle LONG, alle SL
  - Hypothesenbindung und Strategie-Bestaetigung waren schwach
  - `act` entstand trotzdem 50-mal im Feldprotokoll
  Fokus:
  - pruefen, ob allgemeine Reife/Readiness aktuell zu stark gegenueber
    Hypothesenbestaetigung, Familienvertrauen und Strategie-Bestaetigung wirkt
  - keine harte Sperre bauen
  - unbestaetigte Handlungsnaehe eher als hypothetischen Kontakt /
    act-watch / Beobachtungslernen tragen

- [x] `mcm_thought_landkarte.txt` verdichten.
  Ziel:
  - weniger Textlast
  - weniger wiederholte DenkblÃ¶cke
  - qualitativere, energetisch effizientere Landkarte
  - Form/MCM-PrÃ¼fung und DenkÃ¶konomie lesbar halten
  Umsetzung:
  - gleichartige schwache Denkwechsel werden gesammelt statt ausgeschrieben
  - relevante Ereignisse bleiben sichtbar:
    - `act`
    - `replan`
    - Mismatch
    - Denk-Last
    - Denk-Sparbedarf
    - Wahrnehmungsereignis
  - kompakter Block:
    - Form/MCM
    - PrÃ¼fung
    - DenkÃ¶konomie
  - neue Config:
    - `MCM_THOUGHT_LANDKARTE_DEBUG`
    - `MCM_THOUGHT_LANDKARTE_EVERY_N`
    - `MCM_THOUGHT_LANDKARTE_MIN_EVENT`
  Pruefung:
  - Compile OK
  - kompletter Testlauf: 38 Tests OK

- [ ] Naechsten Lauf auf Landkarten-Verdichtung pruefen.
  Fokus:
  - bleibt `mcm_thought_landkarte.txt` deutlich kleiner?
  - werden wichtige Wechsel trotzdem sichtbar?
  - zeigt die Landkarte Denk-Last ohne selbst neue Debug-Last zu erzeugen?
  - passt der Verdichtungsabstand oder muss `MCM_THOUGHT_LANDKARTE_EVERY_N`
    angepasst werden?

- [x] Denk-Last / Denkonomie in die Meta-Regulation aufnehmen.
  Ziel:
  - Denken selbst als MCM-Last sichtbar machen
  - Dauerdenken, Ueberdenken und blindes Vergleichen als Feldbelastung
    erfassen
  - gezieltes Denken bei klarer Form/MCM-Bindung unterstuetzen
  - keine harte Sperre erzeugen, sondern ein wahrnehmbares Signal:
    "Das Denken belastet mich gerade."
  Umsetzung:
  - neue Meta-Werte:
    - `perception_event_strength`
    - `thought_load_pressure`
    - `thought_overprocessing_signal`
    - `thought_economy_need`
    - `thought_release_pressure`
    - `thought_efficiency_support`
  - weiche Wirkung auf Beobachtung, Replan-Druck, Wahrnehmungsdistanz,
    zweite Regulation und Action-Clearance
  - Debug-Ausgabe in `mcm_memory_thinking_protocol.csv`
  Pruefung:
  - Compile OK
  - kompletter Testlauf: 38 Tests OK

- [ ] Naechsten Lauf auf Denkonomie pruefen.
  Fokus:
  - steigt `thought_overprocessing_signal` bei langem Denken ohne klare Form?
  - steigt `thought_efficiency_support`, wenn Denken durch Form, Erinnerung
    und Hypothesenbestaetigung getragen wird?
  - fuehrt hohe Denk-Last eher zu Beobachtung/Distanz statt zu Mikrotrading?
  - bleibt die Wirkung weich und erzeugt keine neue starre Handelssperre?

- [x] DIO-Syntax als ersten echten SpeichertrÃ¤ger umsetzen.
  Ziel:
  - sichtbare Teilform, MCM-Feldwirkung, Erinnerung, Hypothese,
    Konsequenzspur, Reife, Vertrauen und Vorsicht in einer eigenen
    verdichteten DIO-Syntax binden
  - menschliche Namen nur als Decoder/Ãœbersetzung behalten
  - Thought-Landkarte von reinem Debug schrittweise in eine tragende
    interne Syntaxspur Ã¼berfÃ¼hren
  Umsetzung:
  - `dio_form_mcm_token`
  - `dio_form_mcm_sentence`
  - `dio_form_mcm_syntax_state`
  - `form_to_mcm_recall`
  - `mcm_to_form_confirmation`
  - `visual_mcm_context_fit`
  - `visual_mcm_mismatch`
  - `hypothesis_reality_binding`
  - `form_mcm_syntax_density`
  Wichtig:
  - keine harte Pattern-Erkennung
  - keine menschlichen Labels als Innenwahrheit
  - Syntax soll Formseite und MCM-Feldseite organisch koppeln
  PrÃ¼fung:
  - Compile der betroffenen Kernpfade OK
  - kompletter Testlauf: 37 Tests OK

- [ ] NÃ¤chsten Lauf auf Form/MCM-Syntaxspur prÃ¼fen.
  Fokus:
  - entstehen stabile `dio_form_mcm_token`?
  - entstehen deutlich weniger `dio_form_mcm_family_token` als Moment-Tokens?
  - steigt `hypothesis_reality_binding` bei tragenderen Hypothesen?
  - wird `visual_mcm_mismatch` bei schlechten Kontakten sichtbar?
  - bleiben Trade-Anzahl und Regulation ruhig, da die Schicht keine Motorik
    erzwingen darf?
  Status:
  - Lauf 321 geprÃ¼ft
  - 7688 Detailtokens, aber nur 190 Familien-Tokens
  - Verdichtung funktioniert technisch
  - `hypothesis_trust` bleibt 0.0, Familien wirken noch nicht zurÃ¼ck in Reife
    oder Vertrauen

- [x] Form/MCM-Familienreife anbinden.
  Ziel:
  - wiederkehrende `dio_form_mcm_family_token` nicht nur zÃ¤hlen, sondern als
    Reifespur lesen
  - beobachtete Hypothesen und spÃ¤tere Entwicklung pro Familie bewerten
  - daraus weich `hypothesis_trust`, `hypothesis_caution`,
    `hypothesis_reality_binding` und Reorganisationsbedarf speisen
  Wichtig:
  - keine erzwungene Handlung
  - keine harte Regel wie "Familie oft gesehen = Trade"
  - erst Wiederkehr + Bindung + Konsequenz darf Vertrauen bilden
  Umsetzung:
  - eigene `form_mcm_families` in `mcm_thought_memory.json`
  - Rueckfuehrung in `mcm_thought_seed_state`
  - weiche Anbindung in Hypothesen- und Trust-Return-Regulation
  - Debug-Spalten in Thought-Seed- und Thought-Digest-Protokoll
  Pruefung:
  - Compile OK
  - kompletter Testlauf: 38 Tests OK

- [ ] Naechsten Lauf auf Form/MCM-Familienrueckfuehrung pruefen.
  Fokus:
  - steigen `form_mcm_family_maturity` und `form_mcm_family_trust` bei
    wiederkehrenden tragenden Familien?
  - steigt `form_mcm_family_caution` bei Mismatch/offenem Druck?
  - bleibt die Motorik ruhig, also keine Rueckkehr zu Impuls- oder
    Mikrotrading?
  - entstehen weniger reine `withheld`-Zustaende, wenn Familien sichtbar
    reifen?
  - werden Reorganisation und Beobachtung klarer statt nur Hemmung?

- [x] Form/MCM-Syntaxverdichtung nach Lauf 319 korrigiert.
  Befund:
  - 7830 Thought-Zeilen erzeugten 7680 unterschiedliche Moment-Tokens
  - das war zu feingranular und erzeugte zu wenig Wiedererkennung
  Umsetzung:
  - `dio_form_mcm_family_token` ergÃ¤nzt
  - Detailtoken bleibt erhalten
  - Familien-Token nutzt grÃ¶bere Form-/Feld-/Hypothesenlage statt fast jeden
    Moment einzeln zu speichern
  PrÃ¼fung:
  - Compile OK
  - kompletter Testlauf: 37 Tests OK

- [ ] Weitere Refactor-Gegenpruefung gegen alte Programmierung.
  Fokus:
  - `allow_plan=True`-Entstehung gegen alten Pfad pruefen
  - `review_feedback.act_push` gegen `observe_pull` und `replan_pull`
    pruefen
  - Gate-Fallbacks pruefen: echter Entry nur bei `decision_tendency == act`
  - `trade_plan.py` pruefen: Bereichskontakt statt Impulsreaktion
  - Hypothesen-Lernen pruefen: `mcm_thought_memory`, `memory_state`,
    `hypothesis_trust_families`
  - Debug-/Stats-Zaehlung pruefen: Trades, Attempts, Observed, Withheld,
    Replanned
  - Outcome-Rueckkopplung pruefen: keine doppelte positive/negative
    Feldwirkung
  - alte vs. neue Defaultwerte pruefen: keine heimlichen Defaults auf
    `True`, `act`, LONG/SHORT oder hohe Aktionswerte
  Status:
  - `allow_plan=True`-Entstehung geprueft
  - Hypothesenvertrauen formgebunden
  - angereicherte Outcome-Deutung wird wieder in die Bot-Regulation
    synchronisiert
  - `build_meta_regulation_state()` liest die Bot-Outcome-Deutung jetzt in
    den lokalen Hypothesen-Regulationskontext ein

- [ ] Nach naechstem Lauf pruefen:
  - Werden `hypothesis_trust` und `hypothesis_caution` im
    `mcm_field_decision_protocol.csv` ungleich 0?
  - Bleibt die Outcome-Hypothesenwirkung als Nachhall sichtbar, ohne den Lauf
    auf 0 Trades zu hemmen?
  - Ist `courage_hold` nur noch bei niedriger Reife/Readiness/Struktur aktiv?
  - Rutschen `ordinary_structure_reading`-Zustaende weiter ohne tragenden
    Bereichskontakt in echte Trades?
  - Wird `open_hypothesis_needs_reality_contact` sichtbar, ohne dass
    bestaetigte Hypothesen unterdrueckt werden?
  - Bleibt Trade-Anzahl ruhig, ohne dass tragende Strukturhypothesen
    unterdrueckt werden?

Rolle dieser Datei:
- aktive Aufgaben
- nÃ¤chste PrÃ¼fpunkte
- kurze Statusmarkierung

Details, Laufanalysen und Forschungsdeutung gehÃ¶ren nicht hierher.
Regelwerk: `docs/00_regeln/MD_ANWEISUNG.md`.

- [x] `courage_hold` reifeabhaengig gemacht.
  Befund:
  - letzter Snapshot hatte hohe `state_maturity` und `decision_readiness`
  - trotzdem blockierte niedrige `regulated_courage` als absoluter Hold
  Umsetzung:
  - niedriger Mut blockiert nur noch hart, wenn Reife, Readiness, Struktur,
    Struktur-Bearing oder Clearance nicht tragen
  - hohe Reife + weniger Mut wird als vorsichtige Reife behandelt, nicht als
    automatische Blockade
  Pruefung:
  - gezielte Regulation-/Gate-Tests OK
  - kompletter Testlauf: 36 Tests OK
  - Compile der Kernpfade OK
  Naechster Schritt:
  - neuen Lauf pruefen: raus aus 0 Trades, aber nicht zurueck in SL-Serie.

- [x] Lauf 309: 100 % SL-Trades nach Refactor eingegrenzt.
  Befund:
  - Trade-Plan-Formel und aktive Positionsaufloesung sind nicht der direkte
    Bruch gegen den alten Code
  - die Abweichung liegt im Gate/Consent-Pfad: schwache offene oder
    gewoehnliche Strukturdeutungen konnten noch in echte Orders laufen
  Umsetzung:
  - offene Hypothesen brauchen vor Motorik mehr Realitaetkontakt/Bestaetigung
  - gewoehnliche Strukturdeutungen ohne tragenden Bereichskontakt gehen in
    Beobachtung statt Order
  - keine harte Sperre, sondern weiche Kopplung von Hypothese, Innenlage und
    Handlung
  Pruefung:
  - `python -m unittest tests.test_bot_gate_funktions`: 10 Tests OK
  - `python -m unittest discover tests`: 35 Tests OK
  - Compile der Kernpfade OK
  Naechster Schritt:
  - neuen Lauf pruefen: nicht 0 Trades, nicht 100 % SL, weniger
    `ordinary_structure_reading` als echte Order ohne Kontakt.

---

- [x] Altes Entry-Verhalten gegen neues Hypothesenvertrauen geprÃ¼ft.
  Befund:
  - alte Programmierung hatte kein globales
    `dominant_hypothesis_trust_score` im Entry-Gate
  - aktueller Split hatte dadurch ein neues Risiko:
    fremdes/dominantes Hypothesenvertrauen konnte eine aktuelle Form stÃ¼tzen
  Umsetzung:
  - dominantes Hypothesenvertrauen wird nur voll verwendet, wenn
    `dominant_hypothesis_trust_key == form_symbol_id`
  - sonst wirkt es nur als schwache Nachspur plus Vorsichtsdruck
  - gleiche Formbindung jetzt auch in `core/review_feedback.py`, damit
    `act_push` und `possibility_action_support` nicht schon vor dem Gate
    globales Vertrauen als Handlungssupport verwenden
  - `hypothesis_trust_score` und `hypothesis_trust_priority` werden ebenfalls
    formgebunden gedaempft; fremdes Hypothesenvertrauen wird als
    Reality-Check-Druck weitergegeben
  - `core/runtime_entry.py` Ã¼bergibt die aktuelle `form_symbol_id` an den
    Review-Feedback-Pfad
  Pruefung:
  - kompletter Testlauf: 31 Tests OK
  - Compile der geÃ¤nderten Kernpfade OK
  Naechster Schritt:
  - neuen Lauf prÃ¼fen: offene Hypothesen vs. bestÃ¤tigte Strukturinterpretation

- [x] Abweichung bei `decision_strength` zwischen altem Pfad und aktuellem
      Split korrigiert.
  Befund:
  - alter funktioneller Pfad nutzte `max(long_hypothesis, short_hypothesis)`
    aus dem Denkzustand
  - aktueller Split konnte zusÃ¤tzlich `fused_state["decision_strength"]`
    als HandlungsstÃ¤rke einbeziehen
  Risiko:
  - vorverdichtetes Fused-Signal konnte die Meta-Regulation zu frÃ¼h in
    Richtung Handlung schieben
  Umsetzung:
  - `decision_strength` wieder nur aus Denkhypothesen gebildet
  - Regressionstest gegen Fused-Bypass ergÃ¤nzt
  PrÃ¼fung:
  - gezielte Gate-/Regulationstests OK
  - Compile der Kernpfade OK
  NÃ¤chster Schritt:
  - `allow_plan=True`-GrÃ¼nde im Lauf sichtbar machen oder auswerten:
    `field_perception_clear_act`, `plan_allowed`, spÃ¤tere RÃ¼cknahmen

- [x] Aktuellen Regulationspfad gegen die Konstruktion abgeglichen.
  Umsetzung:
  - neue Datei `docs/07_konstruktion/AKTUELLER_REGULATIONS_ABGLEICH.md`
  - Marktpaket-, Runtime-, Meta-Regulations-, Gate-, Non-Action- und
    Entry-AusfÃ¼hrungspfad gegen die Konstruktion geprÃ¼ft
  Befund:
  - Reihenfolge ist grundsÃ¤tzlich wieder korrekt
  - kritische PrÃ¼fpunkte liegen jetzt bei `allow_plan=True`,
    `pre_action_phase`, `review_feedback_state` und Gate-KompatibilitÃ¤tspfad
  NÃ¤chster Schritt:
  - `allow_plan=True`-Entstehung gezielt prÃ¼fen

- [x] Gate-Fallback ohne `decision_tendency` geschlossen.
  Befund:
  - ein KompatibilitÃ¤tspfad konnte LONG/SHORT akzeptieren, wenn kein
    `decision_tendency` im Runtime-Paket lag
  - das ist regulatorisch riskant, weil Hypothese und Handlung wieder
    vermischt werden kÃ¶nnen
  Umsetzung:
  - dieser Fallback wurde aus `bot_gates/entry_decision.py` entfernt
  - `decision_tendency` ist im DIO-Hauptpfad Pflichtinformation
  - Regressionstest ergÃ¤nzt
  PrÃ¼fung:
  - gezielte Gate-/Regulationstests OK
  - kompletter Testlauf: 25 Tests OK
  - Compile der Kernpfade OK
  NÃ¤chster Schritt:
  - `allow_plan=True`-Entstehung in `core/decision_regulation.py` prÃ¼fen

- [x] Regulationskonstruktion als neue Rekonstruktionsbasis dokumentiert.
  Umsetzung:
  - neuer Ordner `docs/07_konstruktion/`
  - alter Pfad `C:\Users\TV\Documents\24.05 v1 MCM_Trading_Brain`
    als Quelle der Extraktion dokumentiert
  - verbindliche Referenz ist jetzt die abstrahierte Konstruktion in
    `docs/07_konstruktion/`, nicht der alte Code selbst
  - Runtime-, Meta-Regulations-, Gate-, Non-Action- und Outcome-Pfad
    beschrieben
  - Checkliste gegen Refactor-BrÃ¼che erstellt
  NÃ¤chster Schritt:
  - aktuellen Code systematisch gegen diese Konstruktion prÃ¼fen
  - Fokus: `allow_plan`, `decision_tendency`, `proposed_decision`,
    Non-Action-Events und Entry-Gate

- [x] Kritisch: Gegensignal durfte nach Refactor als HandlungsstÃ¤rke wirken.
  Befund:
  - neue LÃ¤ufe zeigten wieder willkÃ¼rliches Reaktionstrading
  - Tradefrequenz und Drawdown waren deutlich zu hoch
  - die innere MCM-Regulation wirkte schwach oder Ã¼berfahren
  Ursache:
  - `decision_strength` wurde aus `abs(long_score)` und `abs(short_score)`
    gebildet
  - ein starkes Gegensignal konnte dadurch fÃ¤lschlich als tragende
    HandlungsstÃ¤rke wirken
  Umsetzung:
  - `decision_strength` wieder auf tragende Hypothesenbasis gestellt:
    `long_hypothesis`, `short_hypothesis`, explizite `decision_strength`
  - keine Betragsbildung auf Gegensignalen
  - Gate-Schutz ergÃ¤nzt: `act` mit `allow_plan=False` ruft keinen Brain-Plan
    mehr auf
  PrÃ¼fung:
  - gezielte Regulation-/Gate-Tests OK
  - kompletter Testlauf: 24 Tests OK
  - Compile der betroffenen Kernpfade OK
  - Smoke `python runner.py --smoke --max-windows 1000`: OK, 26 Trades,
    `pnl_netto = 0.8713`
  NÃ¤chster Schritt:
  - frischen Backtest starten und prÃ¼fen, ob `skipped/withheld/observe/replan`
    wieder sichtbar sind und Mikrotrading zurÃ¼ckgeht

- [x] Kritisch: Regulatorischer Bypass Ã¼ber `proposed_decision` behoben.
  Befund:
  - trotz `withheld` blieb die Tradefrequenz hoch
  - bei 17 Prozent Laufstand waren bereits Ã¼ber 100 Trades sichtbar
  Ursache:
  - `allow_plan = False` erzeugte `decision = WAIT`
  - `proposed_decision = LONG/SHORT` blieb als Hypothese erhalten
  - `_compute_runtime_result(...)` konnte diese Hypothese erneut zu `act`
    machen
  Umsetzung:
  - `allow_plan = False` wird jetzt vor LONG/SHORT-Mapping respektiert
  - Nicht-Freigabe wird zu `hold`, `observe` oder `replan`, aber nicht zu
    `act`
  - Regressionstest ergÃ¤nzt
  PrÃ¼fung:
  - gezielte Tests: 6 OK
  - kompletter Testlauf: 22 OK
  - breiter Python-Compile OK
  NÃ¤chster Schritt:
  - neuer Backtestlauf; Tradefrequenz prÃ¼fen
  - falls weiter zu hoch: `allow_plan=True`-Entstehung selbst analysieren

- [x] Kritisch: Meta-Regulationsreset nach Funktionssplit korrigiert.
  Befund:
  - `debug_lauf_271` zeigte 849 Trades, 654 SL und `attempts_withheld = 0`
  - alte VergleichslÃ¤ufe lagen grob bei 285-290 Trades und mehreren tausend
    `withheld`/`skipped` ZustÃ¤nden
  Ursache:
  - `core/decision_regulation.py` setzte spÃ¤ter im Ablauf
    `allow_plan = bool(decision in ("LONG", "SHORT"))`
  - dadurch wurden vorherige innere ZustÃ¤nde wie `hold`, `observe` oder
    `replan` Ã¼berschrieben
  - zusÃ¤tzlich fehlten die alten Config-Schwellen im ausgelagerten Pfad
  Umsetzung:
  - Reset entfernt
  - `_build_pre_action_decision_state(...)` wieder als Quelle der
    Pre-Action-Freigabe genutzt
  - alte Meta-/Struktur-Thresholds aus dem Monolithen zurÃ¼ckgefÃ¼hrt
  - Regressionstest fÃ¼r stabile Aktion und unsichere Nicht-Aktion ergÃ¤nzt
  PrÃ¼fung:
  - gezielte Regulation-/Gate-Tests OK
  - kompletter Testlauf: 21 Tests OK
  - breiter Python-Compile OK
  NÃ¤chster Schritt:
  - neuer vollstÃ¤ndiger Backtest; Tradefrequenz und `withheld/replan/observe`
    gegen die Regulationskonstruktion und alte VergleichslÃ¤ufe prÃ¼fen

- [x] Vergleich alte/neue Programmierung: Entry-Gate nach Funktionssplit korrigiert.
  Befund:
  - alte Version: Tendenzlogik zuerst, Brain-Plan nur bei `act`
  - neue Version: zwischenzeitlich nÃ¤her am fertigen Entry-Plan
  - Folge: zu viele gefÃ¼llte Trades und praktisch kein `withheld`
  Umsetzung:
  - `bot_gates/entry_decision.py` zurÃ¼ck auf `build_runtime_decision_tendency`
  - direkter Brain-Fallback bei fehlender Runtime-Tendenz entfernt
  - unbestÃ¤tigte PlÃ¤ne mit innerem `hold` werden wieder `withheld`
  PrÃ¼fung:
  - Smoke 500 Fenster: 34 Trades
  - Smoke 1000 Fenster: 75 Trades
  - Gate-Tests OK
  - gezielte Tests OK
  - voller Testlauf OK
  - breiter Compile OK
  NÃ¤chster Schritt:
  - vollstÃ¤ndigen Lauf prÃ¼fen; wenn `withheld` weiter zu niedrig bleibt,
    Meta-Regulationsausgabe `pre_action_phase`/`decision_tendency` prÃ¼fen

- [x] Kritisch: Overtrading nach Funktionssplit gestoppt.
  Befund:
  - ein abgebrochener Lauf zeigte ca. 400 Trades bei etwa 50 Prozent Laufstand
  - `debug_lauf_257` zeigte 534 Trades, 401 SL, 133 TP und ca. -32.87 Netto-PnL
  - Ursache war ein Legacy-Direktpfad in `bot_gates/entry_decision.py`
  Umsetzung:
  - direkte Runtime-Entscheidungen mit `LONG`/`SHORT` laufen jetzt immer Ã¼ber
    die innere Handlungsfreigabe
  - Brain-Fallback lÃ¤uft ebenfalls Ã¼ber die Consent-PrÃ¼fung
  - unbestÃ¤tigte Direktimpulse werden zu `WAIT`/`observe` mit
    `proposed_decision`
  - positive Testdoubles brauchen jetzt echte innere Zustimmung
  PrÃ¼fung:
  - Smoke `python runner.py --smoke --max-windows 1000` OK, 72 Trades
  - Gate-Tests OK
  - gezielte Bot-/Gate-/Persistenztests: 6 Tests OK
  - voller Testlauf: 19 Tests OK
  - breiter Python-Compile OK
  NÃ¤chster Schritt:
  - echten Backtestlauf prÃ¼fen; PnL erst nach normalisierter Tradefrequenz
    fachlich bewerten

- [x] Entry-Motorik: Strategie aus bestaetigten Hypothesen verdichten.
  Umsetzung:
  - `hypothesis_trust_score`, `hypothesis_trust_priority`,
    `dominant_hypothesis_trust_score` und beobachtete
    Hypothesenbestaetigung in die innere Handlungsfreigabe eingebunden
  - `strategy_confirmation`, `strategy_rejection` und
    `strategy_trust_bearing` ergaenzt
  - spontane Kontaktlogik weiter zurueckgenommen; gereifte Moeglichkeit wirkt
    ueber Hypothesenvertrauen
  Pruefung:
  - Smoke `python runner.py --smoke --max-windows 300` OK
  - Compile OK
  - gezielte Bot-/Gate-Tests: 5 Tests OK
  - voller Testlauf: 18 Tests OK
  - breiter Python-Compile OK
  Naechster Schritt:
  - echten Lauf auswerten: handelt DIO erkennbar aus
    `strategy_trust_bearing` statt aus Kontaktreiz?

- [x] Entry-Motorik: Impuls darf vorbereiten, aber nicht alleine handeln.
  Umsetzung:
  - innere Handlungsfreigabe in `bot_gates/entry_decision.py` ergaenzt
  - reine Impulsplaene werden zu innerer Verarbeitung/Beobachtung umgeleitet
  - Bereichskontakt braucht zusaetzliche innere Mittragung statt nur
    motorischer Anziehung
  - nach Smoke-Pruefung entschaerft: fehlende volle Zustimmung ist kein
    automatisches Nein; nur klares inneres Gegen-Signal hemmt gereiften
    Bereichskontakt
  - anschliessend fachlich korrigiert: Handlung braucht positives inneres Ja;
    innere Unklarheit wird zu Beobachtung/Hypothesenreifung
  - Nicht-Handlung wird als Konsequenzspur registriert, nicht als
    "verpasster" Trade
  - neue Diagnosefelder: `inner_action_consent`, `inner_action_support`,
    `inner_action_no`, `inner_action_consent_state`
  Pruefung:
  - Compile OK
  - Smoke `python runner.py --smoke --max-windows 300` OK
  - Smoke `python runner.py --smoke --max-windows 20` OK
  - gezielte Bot-/Gate-Tests: 5 Tests OK
  - voller Testlauf: 18 Tests OK
  - breiter Python-Compile OK
  Naechster Schritt:
  - neuen Backtestlauf auswerten: weniger unreife SL-Kontakte, mehr
    observe/replan bei innerem Nein

- [x] Runner: Smoke-Startcheck fuer DIO eingebaut.
  Umsetzung:
  - `runner.py --smoke` ergaenzt
  - `--max-windows` und `--backtest-file` fuer kurze Startchecks ergaenzt
  - Smoke speichert kein Memory
  - Runtime-Thread wird im Backtest-Pfad per `finally` gestoppt
  - aktive Range-Ausgabe auf ASCII `->` umgestellt
  Pruefung:
  - `python runner.py --smoke --max-windows 5` OK
  - Compile OK
  - gezielte Bot-/Gate-Tests: 5 Tests OK
  - voller Testlauf: 18 Tests OK
  - breiter Python-Compile OK
  Naechster Schritt:
  - bei Runner-Abbruch zuerst Smoke mit hoeherer Fensterzahl nutzen

- [x] Refactoring: Meta-Regulation Trust-Return gekapselt.
  Umsetzung:
  - `_build_trust_return_state` in `core/decision_regulation.py` angelegt
  - Trust-Return-/Gedankenbestaetigungsberechnung aus
    `build_meta_regulation_state` herausgezogen
  - Handlungskorrektur bleibt in der Meta-Regulation sichtbar
  - keine MCM-/Trading-Regel geaendert
  Pruefung:
  - Compile OK
  - gezielte Bot-/Gate-Tests: 5 Tests OK
  - voller Testlauf: 18 Tests OK
  - breiter Python-Compile OK
  Naechster Schritt:
  - naechsten geschlossenen Meta-Regulationsblock auslagern

- [ ] Refactoring: Meta-Regulation als naechsten Grossblock zerlegen.
  Befund:
  - `core/decision_regulation.py::build_meta_regulation_state` ist mit
    ca. 1638 Zeilen der groesste verbleibende Mechanikblock
  - naechster sicherer Schnitt sollte klein bleiben, z.B. Rueckgabe-Payload,
    Spannungs-/Trust-Teilachsen oder Initialzustandsaufbau
  Ziel:
  - keine Entscheidungslogik aendern
  - nur fachlich geschlossene Teilachsen auslagern
  - nach jedem Schnitt Compile, gezielte Tests, voller Testlauf und breiter
    Python-Compile

- [x] Refactoring: Felt-State-Rueckgabe und Label gekapselt.
  Umsetzung:
  - `_resolve_market_feel_state` angelegt
  - `_build_felt_state_payload` angelegt
  - `resolve_felt_state` auf 26-Zeilen-Orchestrator reduziert
  - keine Felt-/MCM-/Trading-Regel geaendert
  Pruefung:
  - Compile OK
  - gezielte Bot-/Gate-Tests: 5 Tests OK
  - voller Testlauf: 18 Tests OK
  - breiter Python-Compile OK
  Naechster Schritt:
  - neue Groessenmessung der Restbloecke und naechsten Refactoringblock
    auswaehlen

- [x] Refactoring: Felt-State-Orchestrator bereinigt.
  Umsetzung:
  - unnoetige lokale Achsenzuweisungen aus `resolve_felt_state` entfernt
  - keine ungenutzten lokalen Variablen in `resolve_felt_state` statisch
    gefunden
  - keine Felt-/MCM-/Trading-Regel geaendert
  Pruefung:
  - Compile OK
  - gezielte Bot-/Gate-Tests: 5 Tests OK
  - voller Testlauf: 18 Tests OK
  - breiter Python-Compile OK
  Naechster Schritt:
  - Rueckgabe-/Labelblock im Felt-State strukturieren

- [x] Refactoring: Felt-State-Regulationsblock intern geteilt.
  Umsetzung:
  - `_compute_felt_core_regulation_axes` angelegt
  - `_compute_felt_tension_cause_axes` angelegt
  - `_compute_felt_observation_need` angelegt
  - `_compute_felt_regulation_axes` auf Orchestrierung reduziert
  - keine Felt-/MCM-/Trading-Regel geaendert
  Pruefung:
  - Compile OK
  - gezielte Bot-/Gate-Tests: 5 Tests OK
  - voller Testlauf: 18 Tests OK
  - breiter Python-Compile OK
  Naechster Schritt:
  - Rueckgabe-/Labelblock im Felt-State strukturieren

- [x] Refactoring: Felt-State-Regulationsachsen gekapselt.
  Umsetzung:
  - `_compute_felt_regulation_axes` in `core/felt_state.py` angelegt
  - Druck, Stabilitaet, Alignment, Spannungsursachen und
    Beobachtungsbedarf aus `resolve_felt_state` herausgezogen
  - keine Felt-/MCM-/Trading-Regel geaendert
  Pruefung:
  - Compile OK
  - gezielte Bot-/Gate-Tests: 5 Tests OK
  - voller Testlauf: 18 Tests OK
  - breiter Python-Compile OK
  Naechster Schritt:
  - `_compute_felt_regulation_axes` intern weiter teilen

- [x] Refactoring: Felt-State-Valenzachsen gekapselt.
  Umsetzung:
  - `_compute_felt_valence_axes` in `core/felt_state.py` angelegt
  - Risiko, Gelegenheit und Konflikt aus `resolve_felt_state` herausgezogen
  - keine Felt-/MCM-/Trading-Regel geaendert
  Pruefung:
  - Compile OK
  - gezielte Bot-/Gate-Tests: 5 Tests OK
  - voller Testlauf: 18 Tests OK
  - breiter Python-Compile OK
  Naechster Schritt:
  - Druck-, Stabilitaets- und Tragfaehigkeitsachsen im Felt-State trennen

- [x] Refactoring: Felt-State-Arealachsen gekapselt.
  Umsetzung:
  - `_compute_felt_areal_axes` in `core/felt_state.py` angelegt
  - Arealpraesenz, Arealstuetze und Arealkonfliktdruck aus
    `resolve_felt_state` herausgezogen
  - keine Felt-/MCM-/Trading-Regel geaendert
  Pruefung:
  - Compile OK
  - gezielte Bot-/Gate-Tests: 5 Tests OK
  - voller Testlauf: 18 Tests OK
  - breiter Python-Compile OK
  Naechster Schritt:
  - Risiko- und Gelegenheitsverdichtung im Felt-State trennen

- [x] Refactoring: Felt-State-Eingangsachsen gekapselt.
  Umsetzung:
  - `_collect_felt_input_axes` in `core/felt_state.py` angelegt
  - direkte Rohachsen-Leselogik aus `resolve_felt_state` herausgezogen
  - keine Felt-/MCM-/Trading-Regel geaendert
  Pruefung:
  - Compile OK
  - gezielte Bot-/Gate-Tests: 5 Tests OK
  - voller Testlauf: 18 Tests OK
  - breiter Python-Compile OK
  Naechster Schritt:
  - Areal-/Feldkontaktachsen in eigene Hilfsfunktion zerlegen

- [x] Refactoring: Felt-State in eigenes Core-Modul verschoben.
  Umsetzung:
  - `core/felt_state.py` angelegt
  - `resolve_felt_state` aus dem Brain ausgelagert
  - `build_felt_state` bleibt als duenne Kompatibilitaetsfunktion
  - keine Felt-/MCM-/Trading-Regel geaendert
  Pruefung:
  - Compile OK
  - gezielte Bot-/Gate-Tests: 5 Tests OK
  - voller Testlauf: 18 Tests OK
  - breiter Python-Compile OK
  Naechster Schritt:
  - `core/felt_state.py` intern in kleinere Achsenfunktionen zerlegen

- [x] Refactoring: Review-Feedback-Schicht ausgelagert.
  Umsetzung:
  - `core/review_feedback.py` angelegt
  - `resolve_review_decision_feedback` aus dem Brain ausgelagert
  - `_resolve_review_decision_feedback` bleibt als duenne
    Kompatibilitaetsfunktion
  - keine MCM-/Trading-Regel geaendert
  Pruefung:
  - Compile OK
  - gezielte Bot-/Gate-Tests: 5 Tests OK
  - voller Testlauf: 18 Tests OK
  - breiter Python-Compile OK
  Naechster Schritt:
  - `build_felt_state` vorsichtig in kleinere Achsen-/Stackfunktionen
    zerlegen

- [x] Refactoring: Runtime-Entry-Zustandsaufbau gekapselt.
  Umsetzung:
  - `build_runtime_entry_state_stack` in `core/runtime_entry.py` angelegt
  - Zustandsaufbau aus `_compute_runtime_entry_result` ausgelagert
  - ungenutzte Runtime-Entry-Imports in `MCM_Brain_Modell.py` entfernt
  - keine MCM-/Trading-Regel geaendert
  Pruefung:
  - Compile OK
  - gezielte Bot-/Gate-Tests: 5 Tests OK
  - voller Testlauf: 18 Tests OK
  - breiter Python-Compile OK
  Naechster Schritt:
  - `build_felt_state` oder `_resolve_review_decision_feedback` als naechsten
    Brain-Komplexitaetsblock pruefen

- [x] Refactoring: Runtime-Packet-Action-Cycle ausgelagert.
  Umsetzung:
  - `run_runtime_packet_action_cycle` in `bot_engine/runtime_processing.py`
    angelegt
  - `_run_runtime_packet_action_cycle` in `bot.py` delegiert nur noch
  - Reihenfolge Seed-Memory, Perception-State, Runtime-Step und Action-Cycle
    unveraendert uebernommen
  Pruefung:
  - Compile OK
  - gezielte Bot-/Gate-Tests: 5 Tests OK
  - voller Testlauf: 18 Tests OK
  - breiter Python-Compile OK
  Naechster Schritt:
  - Reststruktur von `bot.py` messen

- [x] Refactoring: Live-Market-Dedupe ausgelagert.
  Umsetzung:
  - `is_duplicate_live_market_packet` in `bot_engine/market_packets.py`
    angelegt
  - `_is_duplicate_live_market_packet` in `bot.py` delegiert nur noch
  - keine Dedupe-Regel geaendert
  Pruefung:
  - Compile OK
  - gezielte Bot-/Gate-Tests: 5 Tests OK
  - voller Testlauf: 18 Tests OK
  - breiter Python-Compile OK
  Naechster Schritt:
  - `_run_runtime_packet_action_cycle` als letzte groessere lokale
    Ablaufmethode pruefen

- [x] Refactoring: Idle-Phasenlogik aus Bot-Fassade verschoben.
  Umsetzung:
  - `clip01` und `resolve_idle_phase_from_state` nach
    `bot_engine/idle_thinking_protocol.py` verschoben
  - `bot.py` behaelt nur duenne Kompatibilitaetswrapper
  - keine MCM-/Trading-Regel geaendert
  Pruefung:
  - Compile OK
  - gezielte Bot-/Gate-Tests: 5 Tests OK
  - voller Testlauf: 18 Tests OK
  - breiter Python-Compile OK
  Naechster Schritt:
  - weitere Restwrapper in `bot.py` pruefen

- [x] Refactoring: Bot-Importgruppen geordnet.
  Umsetzung:
  - lange Importzeilen in `bot.py` in fachliche Importgruppen aufgeteilt
  - keine Logik geaendert
  - `read_memory_state` als bewusste Kompatibilitaetsfassade behalten
  Pruefung:
  - Compile OK
  - gezielte Bot-/Gate-Tests: 5 Tests OK
  Naechster Schritt:
  - Restwrapper in `bot.py` pruefen

- [x] Refactoring: Root-Struktur und Laufzeitartefakte bereinigt.
  Umsetzung:
  - Projektroot auf alte Wrapper-Dateien geprueft
  - keine produktiven alten Root-Wrapper mehr gefunden
  - generierte `__pycache__`-Ordner entfernt
  Pruefung:
  - reine Artefaktbereinigung, keine Mechanikaenderung
  Naechster Schritt:
  - `bot.py` Importgruppen und Restwrapper pruefen

- [x] Refactoring: Legacy-Wrapper nach erfolgreichem Smoke entfernt.
  Umsetzung:
  - `legacy_wrappers/` mit alten Kompatibilitaetsdateien entfernt
  - keine aktive Fachlogik geloescht
  - produktive Imports bleiben auf Paketmodule gerichtet
  Pruefung:
  - Compile OK
  - gezielte Bot-/Gate-Tests: 5 Tests OK
  - voller Testlauf: 18 Tests OK
  - breiter Python-Compile OK
  Naechster Schritt:
  - Importgruppen, Restwrapper und Dokumentationskonsistenz pruefen

- [x] Refactoring: isolierter Backtest-Smoke nach Bot-Auslagerung.
  Umsetzung:
  - echte Bot-/Runtime-Pipeline mit temporaerer CSV und temporaerem
    Arbeitsordner gestartet
  - Runtime-Thread, Feed-Fenster, Queue-Idle, Memory-Save und Debug-Flush
    geprueft
  - echtes `bot_memory/` und echte `debug/`-Laeufe nicht veraendert
  Pruefung:
  - Smoke OK
  - 12 Fenster verarbeitet
  - 7 Attempts erzeugt
  - keine Runtime-Exception
  Naechster Schritt:
  - Datei-/Wrapper-Bereinigung kontrolliert fortsetzen

- [x] Refactoring: Import-/Wrapper-Pruefung nach Handler-Auslagerung.
  Umsetzung:
  - `bot.py` auf ungenutzte Imports geprueft
  - `read_memory_state` als scheinbar ungenutzter Import testweise entfernt
  - Tests zeigten: `bot.read_memory_state` ist externer Patchpunkt
  - Import wiederhergestellt und als Kompatibilitaetsfassade bewertet
  Pruefung:
  - Compile OK
  - gezielte Bot-/Gate-Tests: 5 Tests OK
  - voller Testlauf: 18 Tests OK
  - breiter Python-Compile OK
  Naechster Schritt:
  - Backtest-Smoke mit neuer Modulstruktur statt weiterer Blind-Bereinigung

- [x] Refactoring: Entry-Attempt-Handler ausgelagert.
  Umsetzung:
  - `bot_engine/entry_attempt.py` angelegt
  - `_handle_entry_attempt` aus `bot.py` herausgezogen
  - Entry-Decision, Value-Gate, Live-Order-Submit und Entry-Finalizer-
    Delegation unveraendert uebernommen
  - keine neue Entry- oder MCM-Regel eingebaut
  Pruefung:
  - Compile OK
  - gezielte Bot-/Gate-Tests: 5 Tests OK
  - voller Testlauf: 18 Tests OK
  - breiter Python-Compile OK
  Naechster Schritt:
  - `bot.py` Imports/Wrapper aufraeumen und Strukturstatus festhalten

- [x] Refactoring: Pending-Entry-Handler ausgelagert.
  Umsetzung:
  - `bot_engine/pending_entry.py` angelegt
  - `_handle_pending_entry` aus `bot.py` herausgezogen
  - Live-Cancel, Live-Fill-Handoff, Live-Timeout, Backtest-Fill und
    Backtest-Timeout unveraendert uebernommen
  - keine neue Entry- oder MCM-Regel eingebaut
  Pruefung:
  - Compile OK
  - gezielte Bot-/Gate-Tests: 5 Tests OK
  - voller Testlauf: 18 Tests OK
  - breiter Python-Compile OK
  Naechster Schritt:
  - `_handle_entry_attempt` als letzten grossen Bot-Handler auslagern

- [x] Refactoring: Aktiver Positionshandler ausgelagert.
  Umsetzung:
  - `bot_engine/active_position.py` angelegt
  - `_handle_active_position` aus `bot.py` herausgezogen
  - Positions-Update, Exit-Engine, Live-Exit-Bestaetigung,
    Exit-Kandidaten-Replay und gereifter Exit unveraendert uebernommen
  - keine neue MCM-, Entry- oder Exit-Regel eingebaut
  Pruefung:
  - Compile OK
  - gezielte Bot-/Gate-Tests: 5 Tests OK
  - voller Testlauf: 18 Tests OK
  - breiter Python-Compile OK
  Naechster Schritt:
  - `_handle_pending_entry` als naechsten grossen Bot-Handler auslagern

- [x] Refactoring: Matured-Exit-Signal ausgelagert.
  Umsetzung:
  - `bot_engine/matured_exit.py` angelegt
  - `_resolve_matured_exit_signal` aus `bot.py` herausgezogen
  - Matured-Exit-Auswertung, Debugprotokoll und Episode-Markierung
    unveraendert uebernommen
  - keine Orderausfuehrung geaendert
  Pruefung:
  - Compile OK
  - gezielte Bot-/Gate-Tests: 5 Tests OK
  - voller Testlauf: 18 Tests OK
  - breiter Python-Compile OK
  Naechster Schritt:
  - aktiven Positionshandler weiter zerlegen oder komplett in ein
    Positionsruntime-Modul verschieben

- [x] Refactoring: Target-Expectation ausgelagert.
  Umsetzung:
  - `bot_engine/target_expectation.py` angelegt
  - `_build_target_expectation_state` aus `bot.py` herausgezogen
  - TP-Erreichbarkeit, Erwartungsbruch, Recovery-Watch, semantischer
    Transferstress, Positionspeaks und Debugprotokoll unveraendert uebernommen
  - keine finale Exit-Order- oder Entry-Mechanik geaendert
  Pruefung:
  - Compile OK
  - gezielte Bot-/Gate-Tests: 5 Tests OK
  - voller Testlauf: 18 Tests OK
  - breiter Python-Compile OK
  Naechster Schritt:
  - `_resolve_matured_exit_signal` als naechsten Positionsauswertungsblock
    pruefen

- [x] Refactoring: Exit-Candidate-Observe ausgelagert.
  Umsetzung:
  - `bot_engine/exit_candidate_observe.py` angelegt
  - `_build_exit_candidate_observe_state` aus `bot.py` herausgezogen
  - Candidate-Bewertung, Debug-Protokoll und Episode-Markierung unveraendert
    uebernommen
  - keine Exit-Ausfuehrung oder Ordermechanik geaendert
  Pruefung:
  - Compile OK
  - gezielte Bot-/Gate-Tests: 5 Tests OK
  - voller Testlauf: 18 Tests OK
  - breiter Python-Compile OK
  Naechster Schritt:
  - `target_expectation` auslagern, danach aktiven Positionshandler weiter
    zerlegen

- [x] Refactoring: Position-Intervention ausgelagert.
  Umsetzung:
  - `bot_engine/position_intervention.py` angelegt
  - `_build_position_intervention_state` aus `bot.py` herausgezogen
  - Formeln, Labels, Interventionsdruckzaehler und Debugausgabe unveraendert
    uebernommen
  - keine finale Exit-Order- oder Entry-Mechanik geaendert
  Pruefung:
  - Compile OK
  - gezielte Bot-/Gate-Tests: 5 Tests OK
  - voller Testlauf: 18 Tests OK
  - breiter Python-Compile OK
  Naechster Schritt:
  - `target_expectation` und `exit_candidate_observe` als weitere
    Positionsauswertungs-Helfer pruefen

- [x] Refactoring: Entry-Attempt-Kontext ausgelagert.
  Umsetzung:
  - `bot_engine/entry_attempt_context.py` angelegt
  - `_build_entry_attempt_context` aus `bot.py` herausgezogen
  - `bot.py` behaelt nur den Wrapper
  - keine Order-, Entry-, Exit- oder MCM-Mechanik geaendert
  Pruefung:
  - Compile OK
  - gezielte Bot-/Gate-Tests: 5 Tests OK
  - voller Testlauf: 18 Tests OK
  - breiter Python-Compile OK
  Naechster Schritt:
  - weitere grosse Positions-/Pending-/Entry-Bloecke zuerst nach rein
    lesenden Kontext-/Auswertungshelfern durchsuchen

- [x] Refactoring: Live-Boot-Recovery-Fassade ausgelagert.
  Umsetzung:
  - `bot_engine/live_recovery.py` angelegt
  - Live-Modus-Pruefung, Snapshot-Abfrage, Restart-Recovery-Aufruf und
    Memory-Save aus `bot.py` herausgezogen
  - ungenutzte Imports in `bot.py` entfernt
  - keine Live-Order-, Entry-, Exit- oder MCM-Mechanik geaendert
  Pruefung:
  - Compile OK
  - gezielte Bot-/Gate-Tests: 5 Tests OK
  - voller Testlauf: 18 Tests OK
  - breiter Python-Compile OK
  Naechster Schritt:
  - grosse Positions-/Pending-/Entry-Bloecke nur noch in kleinen,
    nachvollziehbaren Teilschnitten auslagern

- [x] Refactoring: Runtime-Followup ausgelagert.
  Umsetzung:
  - `bot_engine/runtime_followup.py` angelegt
  - Idle-Step, Runtime-Followup-Flush, Idle-Followup und Market-Followup aus
    `bot.py` herausgezogen
  - Memory-/Visualisierungsflusher und Idle-Stepper werden injiziert
  - keine MCM-, Entry- oder Exit-Mechanik geaendert
  Pruefung:
  - Compile OK
  - gezielte Bot-/Gate-Tests: 5 Tests OK
  - voller Testlauf: 18 Tests OK
  - breiter Python-Compile OK
  Naechster Schritt:
  - naechsten isolierten Bot-Block waehlen; bevorzugt Live-Boot-Fassade oder
    Feed-/Packet-Brueckenlogik

- [x] Refactoring: Runtime-Thread-Schicht ausgelagert.
  Umsetzung:
  - `bot_engine/runtime_thread.py` angelegt
  - Start, Stop, Idle-Warten, Queue-State und Runtime-Thread-Initialisierung
    aus `bot.py` herausgezogen
  - Watchdog-Debug bleibt injiziert, keine harte Zusatzkopplung
  - keine MCM-, Entry- oder Exit-Mechanik geaendert
  Pruefung:
  - Compile OK
  - gezielte Bot-/Gate-Tests: 5 Tests OK
  - voller Testlauf: 18 Tests OK
  - breiter Python-Compile OK
  Naechster Schritt:
  - naechsten kleinen Bot-Seiteneffektblock waehlen; grosse Positionslogik nur
    in kontrollierten Teilschnitten anfassen

- [x] Refactoring: Restart-Recovery ausgelagert.
  Umsetzung:
  - `bot_engine/restart_recovery.py` angelegt
  - Wiederherstellung von Pending-Order und aktiver Position aus `bot.py`
    herausgezogen
  - `bot.py` behaelt nur den Wrapper mit `Config`-, Zeit- und
    Episodenmarker-Injektion
  - keine Entry-/Exit-Mechanik, keine MCM-Gewichtung geaendert
  Pruefung:
  - Compile OK
  - gezielte Bot-/Gate-Tests: 5 Tests OK
  - voller Testlauf: 18 Tests OK
  - breiter Python-Compile OK
  Naechster Schritt:
  - naechsten isolierten Bot-Block waehlen; bevorzugt Boot-/Thread- oder
    Positions-Hilfslogik ohne neue Entscheidungsmechanik

- [x] Refactoring: Bot-Market-Packet-Helfer ausgelagert.
  Umsetzung:
  - `bot_engine/market_packets.py` angelegt
  - Window-Normalisierung, Outer-Market-State, Runtime-Market-Packet und
    Live-Dedupe-Key ausgelagert
  - Queue, Dedupe-Zustand und Runtime-Ablauf bleiben in `bot.py`
  Pruefung:
  - Compile OK
  - gezielte Bot-/Gate-Tests: 5 Tests OK
  - direkter Packet-Smoke OK
  Naechster Schritt:
  - voller Testlauf und danach naechsten Market-/Runtime-Helfer waehlen

- [x] Refactoring: Bot-Visualisierungssnapshots ausgelagert.
  Umsetzung:
  - Snapshot-Write-Due, Bundle-Aufbau, Buffering und Flush nach
    `bot_engine/visualization_snapshots.py` verschoben
  - fehlende `Config`/`time`-Injektion nach erstem Testfehler korrigiert
  - keine Entry-/Exit-Mechanik geaendert
  Pruefung:
  - Compile OK
  - Bot-Persistence-Tests: 3 Tests OK
  - direkter Bot-Snapshot-Smoke OK
  Naechster Schritt:
  - voller Testlauf und danach Runtime-Packet-Orchestrierung vorsichtig
    kartieren

- [x] Refactoring: Bot-Regulationssnapshot ausgelagert.
  Umsetzung:
  - `_build_regulation_state_snapshot` delegiert an
    `bot_engine/regulation_snapshot.py::build_regulation_state_snapshot`
  - `_build_regulation_state_delta` delegiert an
    `bot_engine/regulation_snapshot.py::build_regulation_state_delta`
  - keine Orderlogik, keine Entry-/Exit-Mechanik geaendert
  Pruefung:
  - Compile OK
  - Bot-Persistence-Tests: 3 Tests OK
  - direkter Snapshot-/Delta-Smoke OK
  Naechster Schritt:
  - voller Testlauf und danach Visualisierungs-Snapshot-Schreiblogik
    aus `bot.py` ziehen

- [x] Refactoring: Bot-State-Initialisierung ausgelagert.
  Umsetzung:
  - `Bot._initialize_bot_state` delegiert an
    `bot_engine/state_initialization.py::initialize_bot_state`
  - Startwerte und Komponenteninitialisierung aus `bot.py` entfernt
  - Klassen/Funktionen werden injiziert, keine harte Zusatzkopplung
  - keine neue Mechanik, keine neue Gewichtung
  Pruefung:
  - Compile OK
  - Bot-Persistence-Tests: 3 Tests OK
  - direkter Bot-Initialisierungs-Smoke OK
  Naechster Schritt:
  - voller Testlauf und danach Runtime-/Snapshot-Botblock waehlen

- [x] Refactoring: Brain-Datei unter 6000 Zeilen gebracht.
  Umsetzung:
  - ungenutzte Snapshot-/Visualisierungswrapper entfernt
  - Experience-Summary-Helfer direkt aus `core.experience_space` importiert
  - `MCM_Brain_Modell.py` auf ca. 5998 Zeilen reduziert
  - keine neue Mechanik, keine neue Gewichtung
  Pruefung:
  - Compile OK
  - Runtime-/Gate-Integrationstests: 4 Tests OK
  Naechster Schritt:
  - voller Testlauf und danach `bot.py` strukturell angehen

- [x] Refactoring: Runtime Pipeline Snapshot ausgelagert.
  Umsetzung:
  - `build_runtime_pipeline_snapshot` fachlich nach
    `core/runtime_snapshot.py` verschoben
  - `MCM_Brain_Modell.py` behaelt nur Kompatibilitaetswrapper mit Profiling
  - keine neue Mechanik, keine neue Gewichtung
  Pruefung:
  - Compile OK
  - Runtime-/Gate-Integrationstests: 4 Tests OK
  - direkter Snapshot-Smoke OK
  Naechster Schritt:
  - voller Testlauf und danach naechsten klaren Block waehlen

- [x] Refactoring: Runtime Field State ausgelagert.
  Umsetzung:
  - `_derive_runtime_field_state` aus `MCM_Brain_Modell.py` nach
    `core/runtime_field_state.py` verschoben
  - Feldlast, Stabilitaet, Survival-Pressure, Regulatory-Load,
    Action-Capacity und Recovery-Need sind als Runtime-Feldzustand gekapselt
  - keine neue Mechanik, keine neue Gewichtung
  Pruefung:
  - Compile OK
  - Runtime-/Gate-Integrationstests: 4 Tests OK
  Naechster Schritt:
  - voller Testlauf und breite Kompilierung

- [x] Refactoring: Strategic Window ausgelagert.
  Umsetzung:
  - `build_strategic_window_state` aus `MCM_Brain_Modell.py` nach
    `core/strategic_window.py` verschoben
  - `MCM_Brain_Modell.py` importiert die Funktion aus dem neuen Core-Modul
  - keine neue Mechanik, keine neue Gewichtung
  Pruefung:
  - Compile OK
  - Runtime-/Gate-Integrationstests: 4 Tests OK
  Naechster Schritt:
  - voller Testlauf und danach naechsten klaren Brueckenblock waehlen

- [x] Checkpoint und Import-Aufraeumung vor Dateibereinigung.
  Umsetzung:
  - interner Code nutzt jetzt echte Paketmodule statt Root-Wrapper
  - `bot.py`, `MCM_Brain_Modell.py` und Trading-Module auf direkte
    Zielpfade umgestellt
  - Tests von Root-Wrapper-Imports auf Paketmodule umgestellt
  - alte Test-Stubs fuer `bot_engine`-Wrapper entfernt
  - alte Root-Wrapper nach `legacy_wrappers/` verschoben
  - `legacy_wrappers/README.md` als klare Ablagebeschreibung angelegt
  Pruefung:
  - Compile der betroffenen Dateien OK
  - gezielte Runtime-/Gate-/Memory-/Stats-/Persistence-Tests: 13 Tests OK
  - keine direkten internen Root-Wrapper-Imports mehr gefunden
  - voller Unit-Testlauf: 18 Tests OK
  - breite Kompilierung aller Python-Dateien OK
  - Runtime- und Legacy-Wrapper-Import-Smokes OK
  Naechster Schritt:
  - nach einem Backtest-Smoke entscheiden, welche Legacy-Wrapper endgueltig
    entfernt werden koennen

- [x] Stabilisierung Meta-Regulation nach Phase 4ay.
  Umsetzung:
  - `build_meta_regulation_state` wieder als Top-Level-Funktion hergestellt
  - `_apply_open_hypothesis_mutation_state` als Helfer eingefuehrt
  - Export in `core/decision_regulation.py` wieder belastbar
  Pruefung:
  - direkter Smoke-Test fuer `WAIT` und `LONG` OK
  - Compile OK
  - Gate- und Runtime-Integrationstests OK
  - voller Unit-Testlauf: 18 Tests OK
  - breite Kompilierung aller Python-Dateien erfolgreich
  Naechster Schritt:
  - kleiner Runtime-/Backtest-Smoke gegen echte Debug-/Marktdaten

- [x] Refactoring Phase 4ay: Diffuse Open-Development gekapselt.
  Umsetzung:
  - `_build_diffuse_open_development_state` in
    `core/decision_regulation.py` eingefuehrt
  - diffuse Entwicklungsanspannung, Posture-Hinweis und weiche
    Feld-/Handlungsnachregelung gekapselt
  - keine neue DIO-Regel
  Pruefung:
  - Compile OK
  - Gate- und Runtime-Integrationstests OK
  - voller Unit-Testlauf: 18 Tests OK
  Naechster Schritt:
  - spaetere Open-Hypothesis-Mutation kapseln

- [x] Refactoring Phase 4ax: Experience-/Effort-Feedback gekapselt.
  Umsetzung:
  - `_build_experience_effort_feedback_state` in
    `core/decision_regulation.py` eingefuehrt
  - vorheriges Experience-Packet, konstruktive Stimulation,
    Engagement, Reorganisationsdruck, Kontextselektivitaet, Lernzug und
    Effort-Zustand gekapselt
  - bestehende Feld-/Handlungswerte werden wie vorher weich weitergereicht
  - keine neue DIO-Regel
  Pruefung:
  - Compile OK
  - Gate- und Runtime-Integrationstests OK
  - voller Unit-Testlauf: 18 Tests OK
  Naechster Schritt:
  - diffusen Open-Development-/Posture-Block kapseln

- [x] Refactoring Phase 4aw: Temporal-/Spacetime-Regulation gekapselt.
  Umsetzung:
  - `_build_spacetime_regulation_state` in
    `core/decision_regulation.py` eingefuehrt
  - Temporalzustand, Raumzeit-Tiefe, unlokalisierter Druck,
    Memory-/Future-Bearing, Support, Reflexionsbedarf und Zustand gekapselt
  - keine neue DIO-Regel
  Pruefung:
  - Compile OK
  - Gate- und Runtime-Integrationstests OK
  - voller Unit-Testlauf: 18 Tests OK
  - breite Kompilierung aller Python-Dateien erfolgreich
  Naechster Schritt:
  - Experience-Packet-/Effort-Feedbackblock kapseln

- [x] Refactoring Phase 4av: Conscious-Perception-Auslesung gekapselt.
  Umsetzung:
  - `_read_conscious_perception_values` in
    `core/decision_regulation.py` eingefuehrt
  - Labels, innere Haltung, Distanz, Objektkontakt, Feldanhaftung,
    Tonuswerte, Nachbild und Reflexion gekapselt ausgelesen
  - keine neue DIO-Regel
  Pruefung:
  - Compile OK
  - Gate- und Runtime-Integrationstests OK
  - voller Unit-Testlauf: 18 Tests OK
  - breite Kompilierung aller Python-Dateien erfolgreich
  Naechster Schritt:
  - Temporal-/Spacetime-Regulationsblock kapseln

- [x] Refactoring Phase 4au: Neurochemie-/Bewusstseinsachsen gekapselt.
  Umsetzung:
  - `_build_neurochemical_meta_axes` eingefuehrt
  - `_build_conscious_perception_meta_axes` eingefuehrt
  - lange `meta_axes`-Uebergabelisten aus `build_meta_regulation_state`
    entfernt
  - keine neue DIO-Regel
  Pruefung:
  - Compile OK
  - Gate- und Runtime-Integrationstests OK
  - voller Unit-Testlauf: 18 Tests OK
  - breite Kompilierung aller Python-Dateien erfolgreich
  Naechster Schritt:
  - Conscious-Perception-Ausleseblock kapseln

- [x] Refactoring Phase 4at: Pre-Action-Entscheidung gekapselt.
  Umsetzung:
  - `_build_pre_action_decision_state` in `core/decision_regulation.py`
    eingefuehrt
  - Observe/Replan/Hold/Act-Entscheidung mit `allow_*`,
    `rejection_reason` und `pre_action_phase` gekapselt
  - Act-Watch-Nachsteuerung im selben Helfer erhalten
  - Bedingungsreihenfolge bleibt identisch
  - keine neue DIO-Regel
  Pruefung:
  - Compile OK
  - Gate- und Runtime-Integrationstests OK
  - voller Unit-Testlauf: 18 Tests OK
  - breite Kompilierung aller Python-Dateien erfolgreich
  Naechster Schritt:
  - neurochemische Zustandsbildung und Conscious-Perception-Uebergabe
    kartieren

- [x] Refactoring Phase 4as: Open-Hypothesis-Feedback gekapselt.
  Umsetzung:
  - `_build_open_hypothesis_feedback_state` in
    `core/decision_regulation.py` eingefuehrt
  - Outcome-Spuren, Hypothesenspurstaerke, Vertrauen, Vorsicht,
    Reorganisation, Action-Permission, Reality-Check und Reifungszustand
    gekapselt
  - anschliessende `allow_*`-Entscheidung bleibt unveraendert im Hauptblock
  - keine neue DIO-Regel
  Pruefung:
  - Compile OK
  - Gate- und Runtime-Integrationstests OK
  - voller Unit-Testlauf: 18 Tests OK
  - breite Kompilierung aller Python-Dateien erfolgreich
  Hinweis:
  - Root-Dateien wie `exit_engine.py`, `mcm_core_engine.py`,
    `strukture_engine.py` und `place_orders.py` sind Compatibility-Wrapper.
    Aufraeumen erst nach Import-Landkarte.
  Naechster Schritt:
  - `allow_*`-/Pre-Action-Entscheidungsblock kartieren und kapseln

- [x] Refactoring Phase 4ar: Zero-Point-Orientierung gekapselt.
  Umsetzung:
  - `_build_zero_point_orientation_state` in
    `core/decision_regulation.py` eingefuehrt
  - Orientierungsluecke, Blind-Thinking-Load, Zero-Point-Regulation,
    positive Zero-Point-Regulation und Struktur-Orientierungswache
    gekapselt
  - spaetere Verstaerkungen bleiben unveraendert
  - keine neue DIO-Regel
  Pruefung:
  - Compile OK
  - Gate- und Runtime-Integrationstests OK
  - voller Unit-Testlauf: 18 Tests OK
  - breite Kompilierung aller Python-Dateien erfolgreich
  Naechster Schritt:
  - Open-Hypothesis-/Gedankenfeedback-Block kartieren und in Teilbloecke
    zerlegen

- [x] Refactoring Phase 4aq: MCM-Achsenblock gekapselt.
  Umsetzung:
  - `_build_mcm_axis_state` in `core/decision_regulation.py` eingefuehrt
  - vorbewusster Innen-/Aussen-Abgleich, positive/negative Druckachse,
    Ueberdehnung, Rueckfuehrung und MCM-Achsenzustand gekapselt
  - spaetere neurochemische Nachfuehrung bleibt unveraendert
  - keine neue DIO-Regel
  Pruefung:
  - Compile OK
  - Gate- und Runtime-Integrationstests OK
  - voller Unit-Testlauf: 18 Tests OK
  - breite Kompilierung aller Python-Dateien erfolgreich
  Naechster Schritt:
  - Zero-Point-/Orientierungsblock nach der MCM-Achse kapseln

- [x] Refactoring Phase 4ap: Action-Aktivierung gekapselt.
  Umsetzung:
  - `_build_action_activation_state` in `core/decision_regulation.py`
    eingefuehrt
  - regulierter Mut, Courage-Gap, Action-Inhibition, Action-Clearance,
    Plan-Druck und Act-Watch-Bereitschaft gekapselt
  - keine neue DIO-Regel
  Pruefung:
  - Compile OK
  - Gate- und Runtime-Integrationstests OK
  - voller Unit-Testlauf: 18 Tests OK
  - breite Kompilierung aller Python-Dateien erfolgreich
  Naechster Schritt:
  - MCM-Achsenblock mit positiver/negativer Druckachse kapseln

- [x] Refactoring Phase 4ao: Semantische Transferregulation gekapselt.
  Umsetzung:
  - `_build_semantic_transfer_state` in `core/decision_regulation.py`
    eingefuehrt
  - bekannte Formunterstuetzung, Routenvertrautheit,
    semantischer Verschiebungsdruck, Transfer-Bearing, Transfer-Vertrauen,
    Reife-Luecke und Transfer-Fatigue gekapselt
  - Adaptionsphase und Feldmodulation bleiben identisch
  - keine neue DIO-Regel
  Pruefung:
  - Compile OK
  - Gate- und Runtime-Integrationstests OK
  - voller Unit-Testlauf: 18 Tests OK
  - breite Kompilierung aller Python-Dateien erfolgreich
  Naechster Schritt:
  - Courage-/Hemmungsblock nach `regulated_courage` kapseln

- [x] Refactoring Phase 4an: Visuelle Handlungsunsicherheit gekapselt.
  Umsetzung:
  - `_build_visual_action_grounding_state` in
    `core/decision_regulation.py` eingefuehrt
  - Blindhandlungslast, visuelle Handlungsunsicherheit, Objektbindung,
    Grounding-Staerke, ungebundene Resonanz und Grounding-Bedarf gekapselt
  - Wirkung auf Feldbeobachtung/Replan/Action-Support sowie
    Strukturunsicherheit bleibt identisch
  - keine neue DIO-Regel
  Pruefung:
  - Compile OK
  - Gate- und Runtime-Integrationstests OK
  - voller Unit-Testlauf: 18 Tests OK
  Naechster Schritt:
  - semantische Transfer- und Bekanntheitsregulation kapseln

- [x] Refactoring Phase 4am: Strukturaktionsblock gekapselt.
  Umsetzung:
  - `_build_structure_action_state` in `core/decision_regulation.py`
    eingefuehrt
  - Strukturaktions-Bearing, Gap, Unsicherheit und Carrying-Need gekapselt
  - Wirkung auf Feldbeobachtung/Replan/Action-Support bleibt identisch
  - keine neue DIO-Regel
  Pruefung:
  - Compile OK
  - Gate- und Runtime-Integrationstests OK
  - voller Unit-Testlauf: 18 Tests OK
  - breite Kompilierung aller Python-Dateien erfolgreich
  Naechster Schritt:
  - visuelle Handlungsunsicherheit in `build_meta_regulation_state` kapseln

- [x] Refactoring Phase 4al: Orientierungsblock gekapselt.
  Umsetzung:
  - `_build_orientation_state` in `core/decision_regulation.py`
    eingefuehrt
  - Memory-Orientierung, Orientierungsluecke, Blind-Thinking-Load,
    Struktur-Orientierung und Struktur-Orientierungsluecke gekapselt
  - spaeterer zweiter Orientierungsblock bleibt unveraendert
  - keine neue DIO-Regel
  Pruefung:
  - Compile OK
  - Gate- und Runtime-Integrationstests OK
  - voller Unit-Testlauf: 18 Tests OK
  - breite Kompilierung aller Python-Dateien erfolgreich
  Naechster Schritt:
  - Strukturaktionsblock in `build_meta_regulation_state` kapseln

- [x] Refactoring Phase 4ak: Formsymbol-Lernregulation gekapselt.
  Umsetzung:
  - `_apply_form_symbol_learning_regulation` in
    `core/decision_regulation.py` eingefuehrt
  - `learned_development_uncertainty`, Kontaktzustands-Bias und
    Varianten-Lernspannung gekapselt
  - Wirkung auf `field_observation_need`, `field_replan_pressure` und
    `field_action_support` bleibt identisch
  - keine neue DIO-Regel
  Pruefung:
  - Compile OK
  - Gate- und Runtime-Integrationstests OK
  - voller Unit-Testlauf: 18 Tests OK
  - breite Kompilierung aller Python-Dateien erfolgreich
  Naechster Schritt:
  - Orientierungsblock in `build_meta_regulation_state` kapseln

- [x] Refactoring Phase 4aj: Feldregulation aus Meta-Regulation ausgelagert.
  Umsetzung:
  - `_build_field_regulation_state` in `core/decision_regulation.py`
    eingefuehrt
  - Feldinstabilitaet, Beobachtungsbedarf, Replan-Druck und
    Feld-Action-Support gekapselt
  - symbolische Formregulation bleibt in diesem Helfer als bestehende
    Modulation erhalten
  - keine neue DIO-Regel
  Pruefung:
  - Import/Compile OK
  - Gate- und Runtime-Integrationstests OK
  - voller Unit-Testlauf: 18 Tests OK
  - breite Kompilierung aller Python-Dateien erfolgreich
  Naechster Schritt:
  - Formsymbol-Lernunsicherheitsblock in `build_meta_regulation_state`
    kartieren

- [x] Refactoring Phase 4ai: Restlandkarte nach Formsymbol-Auslagerung.
  Ergebnis:
  - `MCM_Brain_Modell.py` ca. 7501 Zeilen
  - `core/form_language.py` ca. 1209 Zeilen
  - `build_form_symbol_state` noch ca. 582 Zeilen, aber deutlich staerker
    Orchestrierung und Memory-Anbindung
  - groesster Einzelblock jetzt:
    `core/decision_regulation.py::build_meta_regulation_state` mit ca. 3311
    Zeilen
  Naechster Schritt:
  - `build_meta_regulation_state` kartieren, bevor dort Teilbloecke
    herausgeloest werden

- [x] Refactoring Phase 4ah: Formsymbol-Basisqualitaet ausgelagert.
  Umsetzung:
  - `_build_form_symbol_base_quality_state` nach `core/form_language.py`
    verschoben
  - Relevance/Bearing/Fragility/Resonance/Zoom/Load-Reduction ausgelagert
  - keine Speicher-Mutation im Helfer
  - keine neue DIO-Regel
  Pruefung:
  - Gate- und Runtime-Integrationstests OK
  - voller Unit-Testlauf: 18 Tests OK
  - breite Kompilierung aller Python-Dateien erfolgreich
  Naechster Schritt:
  - Restlandkarte nach Formsymbol-Auslagerung erstellen oder
    Varianten-Update kapseln

- [x] Refactoring Phase 4ag: Formsymbol-Objektentkopplung ausgelagert.
  Umsetzung:
  - `_build_form_symbol_object_state` nach `core/form_language.py`
    verschoben
  - Objektdistanz, Containment, Feldentkopplung, Split-/Merge-Druck und
    Unsicherheits-Exposition ausgelagert
  - keine Speicher-Mutation im Helfer
  - keine neue DIO-Regel
  Pruefung:
  - Gate- und Runtime-Integrationstests OK
  - voller Unit-Testlauf: 18 Tests OK
  - breite Kompilierung aller Python-Dateien erfolgreich
  Naechster Schritt:
  - Relevance/Bearing/Fragility/Zoom/Load-Reduction kartieren

- [x] Refactoring Phase 4af: Formsymbol-Identitaet ausgelagert.
  Umsetzung:
  - `_build_form_symbol_identity_state` nach `core/form_language.py`
    verschoben
  - Formvektor, Form-Key, Aufloesungsqualitaet, Detaildruck, Scope,
    Abstraktionslevel, Family-Key und Symbol-ID ausgelagert
  - Brain behaelt Speicher- und Bot-State-Anbindung
  - keine neue DIO-Regel
  Pruefung:
  - Gate- und Runtime-Integrationstests OK
  - voller Unit-Testlauf: 18 Tests OK
  - breite Kompilierung aller Python-Dateien erfolgreich
  Naechster Schritt:
  - Objekt-/Entkopplungsblock in `build_form_symbol_state` kartieren

- [x] Refactoring Phase 4ae: Variantenfamilien-Auswertung ausgelagert.
  Umsetzung:
  - `_build_form_symbol_variant_family_state` nach `core/form_language.py`
    verschoben
  - Variantenanzahl, Seen-Summe, Variantenspreizung,
    Unsicherheitsvertrautheit, Bearing-Memory und Lernspannung ausgelagert
  - Brain behaelt Varianten-Update und Variantenbegrenzung
  - keine neue DIO-Regel
  Pruefung:
  - Gate- und Runtime-Integrationstests OK
  - voller Unit-Testlauf: 18 Tests OK
  - breite Kompilierung aller Python-Dateien erfolgreich
  Naechster Schritt:
  - Formvektor-/Scope-Aufbau in `build_form_symbol_state` kartieren

- [x] Refactoring Phase 4ad: Semantische Formverdichtung ausgelagert.
  Umsetzung:
  - `_build_form_symbol_semantic_state` nach `core/form_language.py`
    verschoben
  - Density/Compression/Coherence/Learning-Need/Action-Nearness/Packet-State
    als reine Berechnung ausgelagert
  - keine Speicher-Mutation im Helfer
  - keine neue DIO-Regel
  PrÃ¼fung:
  - Gate- und Runtime-Integrationstests OK
  - voller Unit-Testlauf: 18 Tests OK
  - breite Kompilierung aller Python-Dateien erfolgreich
  NÃ¤chster Schritt:
  - Varianten-/Unsicherheitsfamilien-Block in `build_form_symbol_state`
    kartieren

- [x] Refactoring Phase 4ac: Formsymbol-Item-Statistik ausgelagert.
  Umsetzung:
  - `_update_form_symbol_item_memory_stats` nach `core/form_language.py`
    verschoben
  - Seen/Avg-Vector/Distanz/Varianz/Reife/Stabilitaet/Neuheit/Resonanz
    als reine Berechnung ausgelagert
  - Brain behaelt `form_symbol_space`, Varianten und Persistenz
  - keine neue DIO-Regel
  Pruefung:
  - Gate- und Runtime-Integrationstests OK
  - voller Unit-Testlauf: 18 Tests OK
  - breite Kompilierung aller Python-Dateien erfolgreich
  Naechster Schritt:
  - semantische Verdichtung in `build_form_symbol_state` kartieren

- [x] Refactoring Phase 4ab: Compound-Form-Berechnung ausgelagert.
  Umsetzung:
  - `_build_form_symbol_compound_item` nach `core/form_language.py`
    verschoben
  - Brain behaelt Lesen/Schreiben von `form_symbol_compound_space`
  - reine Compound-Berechnung fuer Formsymbol-Paare ausgelagert
  - keine neue DIO-Regel
  Pruefung:
  - Gate- und Runtime-Integrationstests OK
  - voller Unit-Testlauf: 18 Tests OK
  - breite Kompilierung aller Python-Dateien erfolgreich
  Naechster Schritt:
  - Symbol-Item-Aktualisierung aus `build_form_symbol_state` herausloesen

- [x] Refactoring Phase 4aa: Formsymbol-Lernkern ausgelagert.
  Umsetzung:
  - `_learn_form_symbol_development_item` nach `core/form_language.py`
    verschoben
  - Brain baut den Lernkontext und behaelt Memory-Mutation/Flush
  - reine Berechnung fuer Symbol- und Compound-Nachreifung ausgelagert
  - keine neue DIO-Regel
  Pruefung:
  - Gate- und Runtime-Integrationstests OK
  - voller Unit-Testlauf: 18 Tests OK
  - breite Kompilierung aller Python-Dateien erfolgreich
  Naechster Schritt:
  - `build_form_symbol_state` weiter kartieren

- [x] Refactoring Phase 4z: Kleine Formsymbol-Helfer ausgelagert.
  Umsetzung:
  - `_quantize_form_axis` nach `core/form_language.py`
  - `_extract_outcome_form_symbol_state` nach `core/form_language.py`
  - Brain behaelt Wrapper fuer bestehende Aufrufe
  - keine neue DIO-Regel
  Pruefung:
  - Gate- und Runtime-Integrationstests OK
  - voller Unit-Testlauf: 18 Tests OK
  - breite Kompilierung aller Python-Dateien erfolgreich
  Naechster Schritt:
  - `_update_form_symbol_development_from_outcome` kartieren

- [x] Refactoring Phase 4y: Restlandkarte Brain-Modul erstellt.
  Ergebnis:
  - `MCM_Brain_Modell.py` ca. 7404 Zeilen
  - groesste Restbloecke: Formsymbolik, Runtime-Entry, Felt-State,
    Experience-Orchestrierung, Runtime-Apply
  - naechster sicherer Kandidat: Formsymbolik, weil `core/form_language.py`
    bereits existiert
  Naechster Schritt:
  - `build_form_symbol_state` und
    `_update_form_symbol_development_from_outcome` auf abtrennbare Helfer
    pruefen

- [x] Refactoring Phase 4x: Episode-Review-Berechnung ausgelagert.
  Umsetzung:
  - `_build_episode_review_notes_from_context` nach
    `core/experience_space.py` verschoben
  - `_build_episode_review_notes` bleibt als Brain-Wrapper fuer Bot-Outcome
    und In-Trade-Summary
  - mechanisch uebernommen, keine neue DIO-Regel
  Pruefung:
  - Gate- und Runtime-Integrationstests OK
  - voller Unit-Testlauf: 18 Tests OK
  - breite Kompilierung aller Python-Dateien erfolgreich
  Naechster Schritt:
  - Restlandkarte von `MCM_Brain_Modell.py` erstellen, bevor
    Runtime-Result-Orchestrierung angefasst wird

- [x] Refactoring Phase 4w: Experience-Base-Summary getrennt.
  Umsetzung:
  - `_build_experience_base_summary` eingefuehrt
  - `_build_experience_episode_summary` auf Kontext lesen, Base-Summary
    bauen und Experience-Summary vervollstaendigen reduziert
  - keine neue DIO-Regel
  Pruefung:
  - Gate- und Runtime-Integrationstests OK
  - voller Unit-Testlauf: 18 Tests OK
  - breite Kompilierung aller Python-Dateien erfolgreich
  Stand:
  - Projektstruktur-Auslagerung grob 70 %
  Naechster Schritt:
  - `_build_episode_review_notes` als naechsten grossen Review-/Reife-Block
    pruefen

- [x] Refactoring Phase 4v: Experience-Episode-Leseschicht gebildet.
  Umsetzung:
  - `_read_experience_episode_context` in `MCM_Brain_Modell.py` eingefuehrt
  - Bot-Zustandslesung von Base-Summary-Aufbau getrennt
  - Core bleibt frei von direktem Bot-Zugriff
  - keine neue DIO-Regel
  Pruefung:
  - Gate- und Runtime-Integrationstests OK
  - voller Unit-Testlauf: 18 Tests OK
  - breite Kompilierung aller Python-Dateien erfolgreich
  Naechster Schritt:
  - Base-Summary-Erzeugung aus `_build_experience_episode_summary` weiter
    trennen

- [x] Refactoring Phase 4u: In-Trade-Experience-Helfer ausgelagert.
  Umsetzung:
  - `_compact_in_trade_update_payload` und `_summarize_in_trade_updates`
    nach `core/experience_space.py` verschoben
  - reine Payload-/Listenverdichtung, keine Bot-Mutation
  - mechanisch uebernommen, keine neue DIO-Regel
  Pruefung:
  - Gate- und Runtime-Integrationstests OK
  - voller Unit-Testlauf: 18 Tests OK
  - breite Kompilierung aller Python-Dateien erfolgreich
  Naechster Schritt:
  - Leseschicht fuer `_build_experience_episode_summary` bilden

- [x] Refactoring Phase 4t: Experience-Episode-Summary-Anreicherung ausgelagert.
  Umsetzung:
  - `_complete_experience_episode_summary` nach `core/experience_space.py`
    verschoben
  - Brain liest weiter Bot-Zustand
  - Experience-Space verdichtet die fertige Summary
  - mechanisch uebernommen, keine neue DIO-Regel
  Pruefung:
  - Gate- und Runtime-Integrationstests OK
  - voller Unit-Testlauf: 18 Tests OK
  - breite Kompilierung aller Python-Dateien erfolgreich
  Naechster Schritt:
  - `_build_experience_episode_summary` weiter kartieren und Hilfsleser
    fuer Bot-Zustand bilden

- [x] Refactoring Phase 4s: Episode-Felt-Auswertung ausgelagert.
  Umsetzung:
  - `_derive_felt_label` und `_build_episode_felt_summary` nach
    `core/experience_space.py` verschoben
  - reine Felt-Verdichtung ausgelagert
  - `_build_experience_episode_summary` bleibt wegen Bot-Zustandslesung im
    Brain
  - mechanisch uebernommen, keine neue DIO-Regel
  Pruefung:
  - Gate- und Runtime-Integrationstests OK
  - voller Unit-Testlauf: 18 Tests OK
  - breite Kompilierung aller Python-Dateien erfolgreich
  Naechster Schritt:
  - `_build_experience_episode_summary` in Lese- und Verdichtungsanteile
    kartieren

- [x] Refactoring Phase 4r: Experience-Space-Helfer ausgelagert.
  Umsetzung:
  - neues Modul `core/experience_space.py`
  - Bearing-Delta, neurochemischer Experience-Effekt, Reward-Delta,
    Similarity-Axes, Link-Buckets, Outcome-Protokoll, Episode-Links und
    affektives Strukturprofil ausgelagert
  - `_refresh_experience_space` bleibt als zentrale Orchestrierung im Brain
  - mechanisch uebernommen, keine neue DIO-Regel
  Pruefung:
  - Gate- und Runtime-Integrationstests OK
  - voller Unit-Testlauf: 18 Tests OK
  - breite Kompilierung aller Python-Dateien erfolgreich
  Naechster Schritt:
  - `_refresh_experience_space` kartieren, bevor weitere Experience-Logik
    verschoben wird

- [x] Refactoring Phase 4q: Inner-Context-Cluster ausgelagert.
  Umsetzung:
  - neues Modul `core/inner_context.py`
  - innerer Kontext-Cluster-State, Vektorbildung und Cluster-Memory-Update
    ausgelagert
  - Reward-Delta wird injiziert, keine direkte Experience-Space-Kopplung
  - Bot-Schreibpunkte dokumentiert
  PrÃ¼fung:
  - Gate- und Runtime-Integrationstests OK
  - voller Unit-Testlauf: 18 Tests OK
  - breite Kompilierung aller Python-Dateien erfolgreich
  NÃ¤chster Schritt:
  - Experience-Space nur in kleinen Helfergruppen auslagern

- [x] Refactoring Phase 4p: Inner-Pattern-Identity ausgelagert.
  Umsetzung:
  - neues Modul `core/inner_pattern.py`
  - Wiedererkennung, Stabilitaetsstreak, Pattern-Signatur und Labelableitung
    ausgelagert
  - Bot-Schreibpunkte dokumentiert
  - mechanisch uebernommen, keine neue MCM-Regel
  PrÃ¼fung:
  - Gate- und Runtime-Integrationstests OK
  - voller Unit-Testlauf: 18 Tests OK
  - breite Kompilierung aller Python-Dateien erfolgreich
  NÃ¤chster Schritt:
  - Inner-Context-Cluster als naechsten abgegrenzten Block prÃ¼fen

- [x] Refactoring Phase 4o: Active-Context ausgelagert.
  Umsetzung:
  - neues Modul `core/active_context.py`
  - Replay-Impuls, Nervensystem-Modulation, Decay, Inner-Cluster-Quelle,
    Temporal-Quelle und Refresh ausgelagert
  - `MCM_Brain_Modell.py` behaelt Wrapper fuer bestehende Aufrufe
  - Formeln mechanisch uebernommen, keine neue MCM-Regel
  PrÃ¼fung:
  - Gate- und Runtime-Integrationstests OK
  - voller Unit-Testlauf: 18 Tests OK
  - breite Kompilierung aller Python-Dateien erfolgreich
  NÃ¤chster Schritt:
  - Inner-Pattern-Identity als naechsten mechaniknahen Block nur mechanisch
    und mit Wrappern auslagern

- [x] Refactoring Phase 4n: Feld-/Neuron-Snapshots ausgelagert.
  Umsetzung:
  - neues Modul `debug_tools/field_snapshots.py`
  - Feldtopologie-, Neuron-, Areal-, Aktivitaetsinsel- und Cluster-Snapshot
    aus dem Brain-Modul verschoben
  - `MCM_Brain_Modell.py` behaelt Wrapper fuer bestehende Aufrufe
  - reiner Lese-/Snapshot-Schnitt, keine neue MCM-Regel
  PrÃ¼fung:
  - Gate- und Runtime-Integrationstests OK
  - voller Unit-Testlauf: 18 Tests OK
  - breite Kompilierung aller Python-Dateien erfolgreich
  NÃ¤chster Schritt:
  - Active-Context oder Inner-Pattern-Identity nur nach klarer
    Schreib-/Lesefeld-Markierung auslagern

- [x] Refactoring Phase 4m: Runtime-Bridge ausgelagert.
  Umsetzung:
  - neues Modul `core/runtime_bridge.py`
  - `step_mcm_runtime_idle`, `create_mcm_runtime`, `step_mcm_runtime`
    ausgelagert
  - Runtime-Klasse, Compute und Apply werden injiziert
  - keine neue MCM-Mechanik
  PrÃ¼fung:
  - Gate- und Runtime-Integrationstests OK
  - voller Unit-Testlauf: 18 Tests OK
  - breite Kompilierung aller Python-Dateien erfolgreich
  NÃ¤chster Schritt:
  - vor mechaniknaher Auslagerung Schreib-/Lesefelder je Block markieren

- [x] Refactoring Phase 4l: Brain-Fabrik ausgelagert.
  Umsetzung:
  - neues Modul `core/brain_factory.py`
  - Aufbau von Feld, Cluster, Memory, Self-Model, Attractor und Regulation
    vom Brain-Modul getrennt
  - konkrete Klassen werden injiziert, keine neue Mechanik
  PrÃ¼fung:
  - Gate- und Runtime-Integrationstests OK
  - voller Unit-Testlauf: 18 Tests OK
  - breite Kompilierung aller Python-Dateien erfolgreich
  NÃ¤chster Schritt:
  - Restlandkarte nutzen und danach gezielt sichere Adapter-/Snapshot-BlÃ¶cke
    oder vorsichtig abgegrenzte Lernmechanik auslagern

- [x] Refactoring Phase 4k: Runtime-Klasse ausgelagert.
  Umsetzung:
  - neues Modul `core/runtime.py`
  - `MCMBrainRuntime` steuert Tick, Advance, Impulse und Snapshot-Zustand
  - Brain-Mechanik wird per Callback injiziert
  - Kompatibilitaetsfassade `MCMBrainRuntime` bleibt in `MCM_Brain_Modell.py`
  PrÃ¼fung:
  - Gate- und Runtime-Integrationstests OK
  - voller Unit-Testlauf: 18 Tests OK
  - breite Kompilierung aller Python-Dateien erfolgreich
  NÃ¤chster Schritt:
  - Restlandkarte von `MCM_Brain_Modell.py`: Brain-Mechanik,
    Experience-Space, Signature-/Cluster-Memory, Entry-/Outcome-Mechanik

- [x] Refactoring Phase 4j: Visualisierungs-Snapshots ausgelagert.
  Umsetzung:
  - neues Modul `debug_tools/visualization.py`
  - Snapshot-Pfade, Snapshot-Write, Chart-Snapshot und GUI-Bundle ausgelagert
  - Runtime-Regulations-Transition/Commit-Helfer ausgelagert
  - Brain-Datei behaelt Kompatibilitaetsfassaden
  - `build_runtime_pipeline_snapshot` wird injiziert, kein Importkreis
  PrÃ¼fung:
  - Gate- und Runtime-Integrationstests OK
  - voller Unit-Testlauf: 18 Tests OK
  - breite Kompilierung aller Python-Dateien erfolgreich
  NÃ¤chster Schritt:
  - `MCMBrainRuntime` als Runtime-Klasse prÃ¼fen und ggf. mit Callback-Injektion
    auslagern

- [x] Refactoring Phase 4i: Runtime-Kontext-Refresh gekapselt.
  Umsetzung:
  - `refresh_runtime_context_state` in `core/runtime_commit.py`
  - Experience-Space-Refresh und Active-Context-Refresh gebÃ¼ndelt
  - Active-Context-Commit bleibt im Runtime-Commit-Modul
  - Formeln werden weiterhin injiziert, keine neue MCM-Regel
  PrÃ¼fung:
  - Gate- und Runtime-Integrationstests OK
  - voller Unit-Testlauf: 18 Tests OK
  - breite Kompilierung aller Python-Dateien erfolgreich
  NÃ¤chster Schritt:
  - Restfunktionen in `MCM_Brain_Modell.py` nach Brain-Mechanik,
    Runtime-Orchestrierung und spÃ¤teren Zielmodulen sortieren

- [x] Refactoring Phase 4h: Episode-State gekapselt.
  Umsetzung:
  - `build_visible_episode_state` in `core/runtime_commit.py`
  - `build_internal_episode_state` in `core/runtime_commit.py`
  - `commit_runtime_episode_state` in `core/runtime_commit.py`
  - sichtbare Episode und interne Episode sind getrennt aufgebaut
  - Locked-State-Logik bleibt erhalten, keine neue Handlungsregel
  PrÃ¼fung:
  - Gate- und Runtime-Integrationstests OK
  - voller Unit-Testlauf: 18 Tests OK
  - breite Kompilierung aller Python-Dateien erfolgreich
  NÃ¤chster Schritt:
  - Experience-Space-Refresh und Active-Context-Refresh als Runtime-Bridge
    weiter ordnen

- [x] Refactoring Phase 4g: Runtime-Commit gekapselt.
  Umsetzung:
  - `core/runtime_commit.py` eingefuehrt
  - Temporal-/Felt-/Thought-Advance gekapselt
  - Runtime-Snapshot-/Decision-State-Commit gekapselt
  - Active-Context-Trace-Commit gekapselt
  - Advance-Funktionen werden injiziert, Mechanik bleibt unveraendert
  Pruefung:
  - Gate- und Runtime-Integrationstests OK
  - voller Unit-Testlauf: 18 Tests OK
  - breite Kompilierung aller Python-Dateien erfolgreich
  Naechster Schritt:
  - Episode-Commit vorsichtig kapseln

- [x] Refactoring Phase 4f: Active-Context-Signale entdoppelt.
  Umsetzung:
  - `build_active_context_signal_state` und `merge_active_context_signal`
    in `core/runtime_snapshot.py`
  - Brain-Signal und Episode-Signal nutzen dieselbe Active-Context-Struktur
  - keine Veraenderung der Regulationsmechanik
  Pruefung:
  - Gate- und Runtime-Integrationstests OK
  - voller Unit-Testlauf: 18 Tests OK
  - breite Kompilierung aller Python-Dateien erfolgreich
  Naechster Schritt:
  - `_apply_runtime_result` in klare Commit-Abschnitte zerlegen

- [x] Refactoring Phase 4e: Runtime-Snapshot ausgelagert.
  Umsetzung:
  - neues Modul `core/runtime_snapshot.py`
  - neuronale Felt-Zusammenfassung gekapselt
  - `mcm_runtime_snapshot` und `mcm_runtime_decision_state` werden ueber
    reine Builder erzeugt
  - Bot-State-Commit bleibt in `_apply_runtime_result`
  Pruefung:
  - Gate- und Runtime-Integrationstests OK
  - voller Unit-Testlauf: 18 Tests OK
  - breite Kompilierung aller Python-Dateien erfolgreich
  Naechster Schritt:
  - Active-Context-Signal-Updates entdoppeln und kapseln

- [x] Refactoring Phase 4d: Runtime-Tendenz ausgelagert.
  Umsetzung:
  - neues Modul `core/runtime_tendency.py`
  - `build_runtime_decision_tendency` und `build_runtime_entry_decision`
    bleiben in `MCM_Brain_Modell.py` als Kompatibilitaetsfassade
  - lesende Runtime-Gate-Sicht ist vom Brain-Modul entkoppelt
  - Bot-mutierende Runtime bleibt bewusst noch im Brain
  Pruefung:
  - Gate- und Runtime-Integrationstests OK
  - voller Unit-Testlauf: 18 Tests OK
  - breite Kompilierung aller Python-Dateien erfolgreich
  Naechster Schritt:
  - Runtime-Result-Snapshot und Decision-State-Aufbau kapseln

- [x] Refactoring Phase 4c: Paketstruktur gegen Legacy-Tests stabilisiert.
  Umsetzung:
  - Gate-Kompatibilitaet ueber robusten `bot_gate_funktions.py`-Wrapper
  - alte Patchpunkte `read_memory_state` und `_process_window` wieder
    verfuegbar
  - explizite Attempt-/Outcome-Debugpfade schreiben sofort
  - rohe Outcome-Konsequenzspur und erweiterte emergente Diagnose getrennt
  - Live-Cancel verwendet wieder Positions-Meta als Kontextbasis
  Pruefung:
  - `python -m unittest discover -s tests -p "test_*.py"`: 18 Tests OK
  - `python -m py_compile` fuer alle Python-Dateien erfolgreich
  Naechster Schritt:
  - Brain-Runtime-Grenze vorbereiten und danach Dateistruktur weiter
    aufraeumen

- [x] Refactoring Phase 4b: Interne Imports auf Paketstruktur umgestellt.
  Umsetzung:
  - `bot.py`, `runner.py` und `workspace.py` nutzen neue Paketpfade
  - Root-Wrapper bleiben fuer Legacy-Kompatibilitaet bestehen
  - breite Kompilierung aller Python-Dateien erfolgreich
  Naechster Schritt:
  - Runtime-Grenze im Brain vorbereiten, nicht blind weiter verschieben

- [x] Refactoring Phase 4a: Root-Dateien in Zielpakete verschoben.
  Umsetzung:
  - Memory-State, MCM-Modell, TradeStats, Order-Logik, Order-Helfer,
    CSV-Feed, Exchange-Daten und Gate-Funktionen liegen in Zielpaketen
  - Root-Dateien bleiben als Kompatibilitaetswrapper bestehen
  - breite Kompilierung aller Python-Dateien erfolgreich
  Naechster Schritt:
  - Legacy-Imports in `bot.py`, `runner.py` und Tests schrittweise auf neue
    Paketpfade umstellen

- [x] Refactoring Phase 3l: Debug-Protokolle ausgelagert.
  Umsetzung:
  - `debug_tools/protocols.py` traegt die Runtime-Debug-Protokolle
  - alte Header-Sets im Brain entfernt
  - breite Kompilierung aller Python-Dateien erfolgreich
  Ergebnis:
  - `core`, `memory`, `trading` und `debug_tools` importieren nicht mehr
    direkt aus `MCM_Brain_Modell.py`
  Naechster Schritt:
  - Projektstruktur dokumentieren und Brain-Runtime-Grenze fuer die naechste
    Auslagerungsrunde festlegen

- [x] Refactoring Phase 3k: Form-Symbol-Speicher und Trade-Plan ausgelagert.
  Umsetzung:
  - `memory/form_symbol_memory.py` traegt Laden, Normalisierung, Write und
    Flush des Form-Symbol-Speichers
  - `trading/trade_plan.py` traegt `derive_trade_plan_from_brain`
  - affektive Kontextmodulation liegt in `core/mcm_field.py`
  - breite Kompilierung aller Python-Dateien erfolgreich
  Restkante:
  - `debug_tools/protocols.py` ist noch Adapter auf Brain-Protokollfunktionen
  Naechster Schritt:
  - Projektstruktur bereinigen und Debug-Protokolle separat sauber schneiden

- [x] Refactoring Phase 3j: Thought-State ausgelagert.
  Umsetzung:
  - `build_thought_state` liegt jetzt in `core/decision_regulation.py`
  - Pending-Learning bleibt im Brain, weil dort Signatur- und Cluster-Speicher
    mutiert werden
  - Kompilierung, Importtest und kleine Thought-State-Probe erfolgreich
  Naechster Schritt:
  - vor der groben Ordnerstruktur-Bereinigung Trade-Planung und Runtime-
    Grenzen pruefen

- [x] Refactoring Phase 3i: Meta-Regulation ausgelagert.
  Umsetzung:
  - `build_meta_regulation_state` liegt jetzt in `core/decision_regulation.py`
  - Runtime-Funktionen bleiben im Brain-Modul
  - Neurochemie und bewusste Wahrnehmung werden ueber Core-Module angebunden
  - Kompilierung, Importtest und kleine Meta-Probe erfolgreich
  Naechster Schritt:
  - Runtime-/Trading-Aufteilung gezielt planen: Thought-State, Runtime-Entry
    und Trade-Planung getrennt bewerten

- [x] Refactoring Phase 3h: Aktiver MCM-Kontakt ausgelagert.
  Umsetzung:
  - `build_active_mcm_contact_state` liegt jetzt in `core/mcm_field.py`
  - MCM-Basisklassen werden im Brain ueber `core/mcm_field.py` bezogen
  - Kontaktreife, Raumzeitkontakt, Ueberkopplung, Loslassen und Reframing
    sind vom Brain-Modul entkoppelt
  - Kompilierung, Importtest und kleine Kontakt-Probe erfolgreich
  Naechster Schritt:
  - `build_meta_regulation_state` auf Abhaengigkeiten pruefen und danach
    moeglichst nach `core/decision_regulation.py` auslagern

- [x] Refactoring Phase 3g: Bewusste Wahrnehmung ausgelagert.
  Umsetzung:
  - `build_conscious_perception_state` liegt jetzt in `core/perception.py`
  - bewusster Kontakt, Nachhall, Distanzierung, Innen-/Aussenabgleich und
    innere Haltung sind vom Brain-Modul entkoppelt
  - Kompilierung, Importtest und Conscious-Perception-Probe erfolgreich
  Naechster Schritt:
  - aktiven MCM-Kontakt nach `core/mcm_field.py` auslagern

- [x] Refactoring Phase 3f: Neurochemie ausgelagert.
  Umsetzung:
  - `core/neurochemistry.py` traegt jetzt `build_neurochemical_state`
  - Neurochemie ist vom Brain-Modul entkoppelt und ohne Trading-Side-Effects
  - Erfahrungs-Neurochemie bleibt vorerst im Brain, weil dort noch Kontext-
    und Erfahrungshelper haengen
  - Kompilierung, Importtest und kleine Neurochemie-Probe erfolgreich
  Naechster Schritt:
  - bewusste Wahrnehmungsschicht pruefen und gegebenenfalls nach
    `core/perception.py` auslagern

- [x] Refactoring Phase 3e: Perception teilweise ausgelagert.
  Umsetzung:
  - `core/perception.py` traegt Weltzustand, aeusseres Sehen,
    Processing-State und allgemeinen Perception-State
  - innere MCM-Feldwahrnehmung bleibt vorerst im Brain-Modul
  - Kompilierung, Importtest und Perception-Probe erfolgreich
  Naechster Schritt:
  - Neurochemie nach `core/neurochemistry.py` auslagern

---

- [x] Refactoring Phase 3d: Temporal-/Raumzeit-Wahrnehmung ausgelagert.
  Umsetzung:
  - `core/temporal_perception.py` traegt Temporal Identity, Wiederkehr,
    Nachhall, Gedaechtnistiefe, Zukunftstiefe und Raumzeit-Regulation
  - `MCM_Brain_Modell.py` importiert die Temporal-Funktionen nur noch
  - Kompilierung, Importtest und kleine Temporal-Probe erfolgreich
  Naechster Schritt:
  - Perception-Schichten nach `core/perception.py` auslagern

---

- [x] Refactoring Phase 3c: Hypothesen-Lernen ausgelagert.
  Umsetzung:
  - `core/hypothesis_learning.py` traegt offene Hypothesenbewertung,
    Beobachtungsreife, Trust, Frust, Distanz und Moeglichkeitsreife
  - `trade_stats.py` bleibt Speicher- und Statistikbesitzer
  - Methoden in `TradeStats` sind jetzt Wrapper auf die Core-Funktionen
  - Kompilierung, Importtest und Berechnungsprobe erfolgreich
  Naechster Schritt:
  - Perception-/Temporal-Bloecke aus `MCM_Brain_Modell.py` auslagern

---

- [x] Refactoring Phase 3b: DIO-Formsprache ausgelagert.
  Umsetzung:
  - `_build_dio_form_language_state` liegt jetzt in `core/form_language.py`
  - `MCM_Brain_Modell.py` importiert die Satzschicht nur noch
  - keine Aenderung an Entscheidungslogik oder Trading-Mechanik
  - Kompilierung und Importtest erfolgreich
  Naechster Schritt:
  - Hypothesen-Lernen nach `core/hypothesis_learning.py` herausloesen
  - dabei zuerst nur Analyse-/Trust-Werte kapseln, keine neue Regelmechanik

---

- [x] Refactoring Phase 3a: Thought-Memory-Speicher ausgelagert.
  Umsetzung:
  - `core/thought_memory.py` traegt jetzt Laden, Normalisierung,
    Familienbildung, Update, Write und Flush fuer `mcm_thought_memory.json`
  - `MCM_Brain_Modell.py` importiert die Thought-Memory-Funktionen nur noch
    als Kompatibilitaet
  - `memory/thought_memory_store.py` bleibt als Speicher-Zieladapter nutzbar
  - Kompilierung, Importtest und isolierter Write-Test erfolgreich
  Folgestand:
  - DIO-Formsprache wurde danach nach `core/form_language.py` ausgelagert
  - danach Hypothesen-Vertrauen nach `core/hypothesis_learning.py`

---

- [x] Lauf 8 bis 10 nach Hypothesenreifung ausgewertet.
  Befund:
  - Lauf 8: PnL ca. `+20.89`
  - Lauf 9: PnL ca. `+30.28`, aber hoeherer Drawdown ca. `17.45 %`
  - Lauf 10: PnL ca. `+32.37` bei niedrigem Drawdown ca. `6.63 %`
  - Short ist klarer Haupttraeger
  - Long bleibt wechselhaft
  - Hypothesenwerte trennen weiter sauber zwischen Handlung, Watch und Replan

- [ ] Reorganisierende Hypothesen als innere Replay-/Verdauungsspur schaerfen.
  Ziel:
  - `open_hypothesis_reorganizing` nicht direkt als Handlungskraft lesen
  - diese Spur als Trainingsmaterial fuer spaetere Strukturkontakte nutzen
  - bestaetigte Wiederkehr in Vertrauen umwandeln
  - keine harte Sperre, sondern Reifung ueber wiederholten Kontakt

---

- [x] Lauf 6 und 7 nach Hypothesenreifung ausgewertet.
  Befund:
  - Lauf 6: PnL ca. `+16.56`
  - Lauf 7: PnL ca. `+25.08`
  - Lauf 7 hat deutlich niedrigeren Drawdown mit ca. `7.26 %`
  - Short wird klarer Haupttraeger
  - neue Hypothesenwerte werden im Field-Protokoll geschrieben
  - `act` zeigt hoeheres `open_hypothesis_action_permission`
  - `replan` zeigt hoehere Lernladung und Realitaetspruefung

- [ ] Lauf 8 nach Hypothesenreifung pruefen.
  Ziel:
  - bestaetigen, ob Lauf 7 eine stabile Reifewirkung oder ein Einzelpeak war
  - pruefen, ob Short weiter Haupttraeger bleibt
  - Long-Unruhe beobachten
  - Drawdown und `open_hypothesis_reality_check_need` verfolgen
  - keine harte Richtungsvorgabe ableiten

---

- [x] Hypothesenreifung gegen vorsichtige Hemmung verfeinert.
  Umsetzung:
  - `open_hypothesis_confirmation_weight`
  - `open_hypothesis_learning_charge`
  - `open_hypothesis_action_permission`
  - `open_hypothesis_reality_check_need`
  - reorganisierende Hypothesen wirken staerker als Reflexions- und
    Lernspannung, weniger als direkter Motorimpuls
  - Protokolle wurden um die neuen Werte erweitert

- [ ] Lauf 6 nach Hypothesenreifung pruefen.
  Ziel:
  - Verteilung der vier neuen Hypothesenwerte auswerten
  - pruefen, ob `open_hypothesis_reorganizing` weniger direkt verlustreich
    handelt
  - pruefen, ob `open_hypothesis_carried` weiterhin tragend bleibt
  - besonders Long-PnL, `act_watch`, `replan`, `open_hypothesis_reality_check`
    und `plan_allowed` beobachten

---

- [x] Lauf 5 nach MCM-Spannungsachse ausgewertet.
  Befund:
  - PnL ca. `+4.32`
  - Long nur noch leicht positiv mit ca. `+0.81`
  - Short positiv mit ca. `+3.52`
  - MCM-Achse bleibt stabil: fast alles `0`, kein positiver Ueberdehnungsmodus
  - Rueckgang kommt eher aus Hypothesenreifung, weniger bestaetigter Struktur
    und mehr Zurueckhaltung

- [ ] Hypothesenreifung gegen vorsichtige Hemmung pruefen.
  Ziel:
  - `open_hypothesis_carried`, `open_hypothesis_burdened` und
    `open_hypothesis_reorganizing` genauer in Handlung / Beobachtung /
    Replay koppeln
  - reorganisierende Hypothesen nicht als Handlungskraft lesen
  - keine harte Sperre bauen, sondern eine weichere Reifedifferenzierung
    zwischen tragender Hypothese, belasteter Hypothese und Lernspannung

---

- [ ] Gedankenraum nach frischem Lauf 1 auf Speicherwachstum prÃ¼fen.
  Befund:
  - `mcm_thought_memory.json` ist nach einem Lauf bereits ca. `8.7 MB`
  - Thought-Seed-Protokoll ca. `10 MB`
  - DIO bildet viele neue Syntax- und Gedankenfamilien
  Ziel:
  - keine harte KÃ¼rzung
  - Verdichtung prÃ¼fen: Ã¤hnliche Gedankenfamilien zusammenfÃ¼hren, ohne die
    emergente Varianz zu zerstÃ¶ren
  - unterscheiden zwischen wertvoller Gedankenreifung und reiner Wiederholung

- [ ] Lauf 2 mit neuem Thought-Memory auswerten.
  Ziel:
  - prÃ¼fen, ob `open_hypothesis_reorganizing_memory` in tragendere ZustÃ¤nde
    Ã¼bergeht
  - prÃ¼fen, ob `hypothesis_trust` steigt
  - prÃ¼fen, ob `inner_outer_alignment` und `temporal_self_consistency`
    stabiler werden
  - prÃ¼fen, ob Long/Short-Verhalten ausgewogener oder bewusster wird

- [x] Lauf 2 mit neuem Thought-Memory ausgewertet.
  Befund:
  - PnL ca. `+5.08`
  - Trades sinken von `409` auf `345`
  - Thought-Memory wÃ¤chst kaum weiter und wirkt daher eher wiederverwendend
    als explosionsartig
  - `open_hypothesis_carried_memory` steigt deutlich von `340` auf `927`
  - `hypothesis_trust` steigt von ca. `0.023` auf ca. `0.059`
  - `inner_outer_alignment` und `temporal_self_consistency` steigen nur leicht
  NÃ¤chster Schritt:
  - Lauf 3 prÃ¼fen, ob getragene Hypothesen weiter zunehmen
  - danach Thought-Memory-Verdichtung prÃ¼fen, falls Wiederholungen entstehen

- [x] Lauf 3 mit neuem Thought-Memory ausgewertet.
  Befund:
  - PnL ca. `+13.01`
  - Thought-Memory bleibt kontrolliert bei ca. `8.74 MB`
  - `observation_learning.maturity_trust` steigt auf ca. `0.535`
  - `observation_learning.action_pressure` sinkt auf ca. `0.463`
  - `hypothesis_trust` fÃ¤llt gegenÃ¼ber Lauf 2 wieder auf ca. `0.030`
  - `open_hypothesis_carried_memory` fÃ¤llt auf `429`
  Deutung:
  - Ã¤uÃŸere Performance verbessert sich, aber innere Hypothesen-Sicherheit
    bleibt instabil
  - DIO wirkt funktionaler, aber noch nicht wirklich selbstsicher

- [ ] Lauf 4 als StabilitÃ¤tsprÃ¼fung nach Lauf 3 auswerten.
  Ziel:
  - prÃ¼fen, ob PnL-Steigerung stabil oder laufabhÃ¤ngig ist
  - prÃ¼fen, ob `act_watch` konstruktiv bleibt
  - prÃ¼fen, ob `position_nervousness` sinkt oder weiter hoch bleibt
  - prÃ¼fen, ob Thought-Memory weiter verdichtet bleibt

- [x] Lauf 4 als StabilitÃ¤tsprÃ¼fung nach Lauf 3 ausgewertet.
  Befund:
  - PnL ca. `+31.26`
  - Entwicklungsreihe: `+3.57`, `+5.08`, `+13.01`, `+31.26`
  - Thought-Memory bleibt kontrolliert bei ca. `8.75 MB`
  - Long wird leicht positiv, Short bleibt HaupttrÃ¤ger
  - `hypothesis_trust` bleibt niedrig, also Performance steigt schneller als
    inneres Selbstvertrauen
  Deutung:
  - starker Hinweis auf kognitives ZÃ¼nden / bessere Handlungskopplung
  - noch kein endgÃ¼ltiger Nachweis, weitere LÃ¤ufe nÃ¶tig

- [ ] EntwicklungsÃ¼bersicht fÃ¼r LÃ¤ufe nach frischem Memory bauen.
  Ziel:
  - pro Lauf PnL, Trades, Long/Short-PnL, Thought-Memory-GrÃ¶ÃŸe,
    `hypothesis_trust`, `open_hypothesis_carried_memory`, `act_watch`,
    Observation-Maturity und Action-Pressure nebeneinander auswerten
  - sichtbar machen, ob DIO wirklich reift oder nur laufabhÃ¤ngig variiert

- [x] EntwicklungsÃ¼bersicht fÃ¼r LÃ¤ufe nach frischem Memory gebaut.
  Datei:
  - `docs/02_status/ENTWICKLUNGSUEBERSICHT.md`
  EnthÃ¤lt:
  - Lauf 1 bis 4
  - PnL-Reihe `+3.57 -> +5.08 -> +13.01 -> +31.26`
  - Thought-ProtokollgrÃ¶ÃŸe
  - Hypothesen- und Observation-Werte
  NÃ¤chster Schritt:
  - nach Lauf 5 fortschreiben
  - prÃ¼fen, ob Lauf 4 ein getragener Reifungssprung oder eine starke
    Varianzphase war

- [x] Lauf 5 ausgewertet und EntwicklungsÃ¼bersicht fortgeschrieben.
  Befund:
  - PnL ca. `+20.97`
  - schwÃ¤cher als Lauf 4, aber weiter deutlich Ã¼ber Lauf 1 bis 3
  - Short bleibt stark mit ca. `+29.62`
  - Long kippt wieder negativ mit ca. `-8.65`
  - mehr `WAIT`, `hold`, `fused_score_too_low` und `maturity_block`
  - `open_hypothesis_carried_memory` steigt auf `627`
  Deutung:
  - eher vorsichtige Reorganisation als Zusammenbruch
  - Long-Bereich bleibt instabil und sollte in Lauf 6 beobachtet werden

- [ ] Lauf 6 auf Long-spezifische Unsicherheit prÃ¼fen.
  Ziel:
  - Long-PnL und Long-Trades prÃ¼fen
  - prÃ¼fen, ob `maturity_block` und `fused_score_too_low` weiter steigen
  - prÃ¼fen, ob getragene Hypothesen trotz Vorsicht weiter zunehmen
  - keine harte Long-Regel ableiten

- [x] MCM-Spannungsachse `-- - 0 + ++` umgesetzt.
  Umsetzung:
  - positive MCM-Seite wird nicht mehr automatisch als Ruhe/Support gelesen
  - neue Werte:
    - `positive_expansion_pressure`
    - `negative_contraction_pressure`
    - `positive_overextension`
    - `positive_return_pressure`
    - `mcm_axis_displacement`
    - `mcm_axis_tension`
    - `mcm_axis_state`
    - `positive_zero_point_regulation`
  - positive Ãœberdehnung kann weich Beobachtung, `act_watch`, Reflexion und
    RÃ¼ckfÃ¼hrung zur 0 erhÃ¶hen
  - keine harte Long-/Short-Regel
  PrÃ¼fung:
  - `python -m py_compile .\MCM_Brain_Modell.py .\bot.py .\trade_stats.py`
    lÃ¤uft sauber

- [ ] NÃ¤chsten Lauf nach MCM-Spannungsachse auswerten.
  Ziel:
  - Verteilung von `mcm_axis_state` prÃ¼fen
  - `positive_return_pressure` bei Long vs Short vergleichen
  - prÃ¼fen, ob `positive_expansion_zero_point` oder
    `positive_expansion_observe` sichtbar werden
  - prÃ¼fen, ob Long weniger aus positiver Ãœberdehnung handelt

- [x] Debug LÃ¤ufe 1-3 nach MCM-Spannungsachse ausgewertet.
  Befund:
  - Lauf 1: ca. `-0.01`
  - Lauf 2: ca. `+3.13`
  - Lauf 3: ca. `+22.84`
  - Short bleibt HaupttrÃ¤ger
  - Long bleibt instabil
  - `action_clearance` sinkt, `action_inhibition` steigt
  - `act_watch` steigt deutlich
  Deutung:
  - Reorganisationskurve statt Zusammenbruch
  - DIO wird vorsichtiger/gebundener und in Lauf 3 trotzdem deutlich stÃ¤rker

- [x] Field-Protokoll fÃ¼r MCM-Spannungsachse korrigiert.
  Befund:
  - LÃ¤ufe 1-3 hatten die Mechanik aktiv, aber die neuen Achsen wurden im
    `mcm_field_decision_protocol.csv` noch nicht ausgeschrieben
  Umsetzung:
  - Header und Row um die neuen MCM-Achsen ergÃ¤nzt
  PrÃ¼fung:
  - `python -m py_compile .\MCM_Brain_Modell.py .\bot.py .\trade_stats.py`
    lÃ¤uft sauber

- [ ] NÃ¤chsten Lauf mit korrigiertem Field-Protokoll prÃ¼fen.
  Ziel:
  - direkte Verteilung von `mcm_axis_state`
  - Long vs Short bei `positive_expansion_pressure`
  - Long vs Short bei `positive_return_pressure`
  - Auftreten von `positive_zero_point_regulation`
  - GrÃ¼nde `positive_expansion_zero_point` und `positive_expansion_observe`


- [x] `mcm_thought_memory.json` gegen Windows-Dateilock abgesichert.
  Umsetzung:
  - robuste atomare Schreibfunktion mit eindeutiger Temp-Datei
  - Retry bei `PermissionError`
  - Fehlerprotokoll statt Lauf-Crash
  - Thought-Memory bleibt dirty und kann spÃ¤ter erneut speichern
  - Formsymbol-Memory nutzt dieselbe robuste Schreibfunktion

- [x] Debug-Ausgabe in fachliche Unterordner aufgeteilt.
  Umsetzung:
  - `DEBUG_GROUPED_DIRS = True`
  - automatische Sortierung zentral in `debug_reader`
  - `gui/`: PnL-/Stats-Dateien
  - `core/`: Kernentscheidungen, Outcomes, Thought-Seeds, Neurotransition
  - `language/`: Formsprache und Gedankenspur
  - `perception/`: Sehen, Kontakt, strategische Fenster
  - `position/`: Position und Exit-Kandidaten
  - `performance/`: Laufzeit-/Schreibprofile
  - Brain-Mechanik unverÃ¤ndert

- [ ] Neuen Lauf 1 auf Debugstruktur prÃ¼fen.
  Ziel:
  - `debug/debug_lauf_1/gui/trade_equity.csv` wird geschrieben
  - `debug/debug_lauf_1/gui/trade_stats.json` wird geschrieben
  - Kernprotokolle landen in `core/`
  - DIO-Syntax/Thought-Protokolle landen in `language/` bzw. `core/`
  - keine alten ungeordneten Debugdateien direkt im Laufwurzelordner

- [x] Neue Memory und neue Debugs fÃ¼r DIO-Form-Language-Start vorbereitet.
  Umsetzung:
  - aktive Memory-Dateien archiviert
  - aktive DebuglÃ¤ufe archiviert
  - `debug/` ist leer fÃ¼r neue LÃ¤ufe
  - nÃ¤chster Lauf baut Welt-, Form- und Gedankenerfahrung neu auf

- [ ] Neuen Lauf 1 nach Memory-/Debug-Neustart prÃ¼fen.
  Ziel:
  - neue Memory-Dateien entstehen sauber
  - neuer Debuglauf entsteht im leeren `debug/`
  - DIO-Syntaxspuren werden geschrieben:
    `dio_world_experience_anchor`, `dio_thought_experience_anchor`,
    `dio_dialogue_bridge_sentence`
  - erste neue Thought-Families und Formfamilien aus frischem Speicher
    auswerten

- [x] DIO Form Language Core als zentrale innere Syntaxschicht angelegt.
  Umsetzung:
  - `dio_language_sentence` bindet Form, Feld, Gedanke, Herkunft, Reifung,
    Handlung und Kontext
  - `dio_world_experience_anchor` und `dio_thought_experience_anchor`
    trennen weltliche Erfahrung und Gedankenerfahrung
  - `dio_dialogue_bridge_sentence` bildet die verdichtete BrÃ¼cke zwischen
    FÃ¼hlen, WeltgedÃ¤chtnis, GedankengedÃ¤chtnis, Hypothese und Handlung
  - `dio_syntax_signature`, `dio_language_state`, `dio_syntax_origin`,
    `dio_syntax_density`, `dio_syntax_compression` und
    `dio_syntax_coherence` ergÃ¤nzt
  - Thought-Memory speichert die Satzspur bei Seeds und Familien mit
  - Thought-Seed-Protokoll schreibt die neue Syntaxdiagnose

- [ ] NÃ¤chsten Lauf auf DIO-Syntax prÃ¼fen.
  Ziel:
  - wiederkehrende `dio_syntax_signature` zÃ¤hlen
  - `dio_language_state` nach PnL, Phase und emergenter Struktur auswerten
  - prÃ¼fen, ob `dio_syntax_compression` kognitive Last reduziert
  - prÃ¼fen, ob `dio_syntax_origin` mit semantischer Herkunft zusammenpasst
  - prÃ¼fen, ob Weltanker und Gedankenanker sauber getrennt bleiben

- [x] Historische Hypothesen-/Handlungsgewichtung sauber zusammenfÃ¼hren.
  Ziel:
  - Entscheidungen nicht nur nach Momentreiz bewerten
  - getragene, belastete und reorganisierende Hypothesen als GedÃ¤chtnisspur
    fÃ¼hren
  - `form_symbol_*`, Kontextcluster, Beobachtungsreife, Thought-Families und
    `open_hypothesis_learning` zu einer weichen Rezeptorschicht verbinden
  - keine harte Sperre, sondern organische Reifung, Vertrauen, Vorsicht,
    Replay und Reframing

- [ ] NÃ¤chsten Lauf auf historische Hypothesen-/Handlungsgewichtung prÃ¼fen.
  Ziel:
  - `hypothesis_trust`, `hypothesis_caution` und
    `hypothesis_reorganization_weight` im Feldprotokoll auswerten
  - prÃ¼fen, ob `action_weight` und `decision_weight` weniger breit hemmen als
    die vorige Reifeschicht
  - besonders `ordinary_structure_reading`, `open_hypothesis_carried` und
    `open_hypothesis_reorganizing` vergleichen

- [x] Lauf 63 ausgewertet.
  Befund:
  - PnL ca. `+40.14`
  - Drawdown ca. `6.63 %`, ruhiger als Lauf 61/62
  - Short bleibt tragend: ca. `+30.08`
  - `family_total_seen`: `3351`
  - Top-Familien liegen jetzt Ã¼ber `100` Wiederholungen
  - offene Strukturhypothese wieder stÃ¤rker negativ: ca. `-33.91`

- [ ] Offene Strukturhypothesen mit Thought-Family-Kontext analysieren.
  Ziel:
  - belastete offene Hypothesen nach Familien gruppieren
  - tragende offene Hypothesen nach Familien gruppieren
  - prÃ¼fen, ob bestimmte Familien immer wieder zu frÃ¼h motorisch werden
  - keine Sperre bauen, sondern Reifungs-/Distanzierungslogik verbessern


- [x] Debug-Schreiblast auf Kern-Diagnose entschÃ¤rft.
  Umsetzung:
  - neues Standardprofil `DIO_CORE_DEBUG`
  - schwere Dauerprotokolle im Standardlauf aus
  - `trade_stats.json` und `trade_equity.csv` bleiben als PnL-/GUI-Spur aktiv
  - Outcome, Feldentscheidung, Neurotransition, Positionslast und
    Thought-Seeds bleiben sichtbar
  - Thought-Memory und Thought-Families bleiben aktiv
  - Mechanik unverÃ¤ndert, nur Diagnoseausgabe reduziert

- [ ] NÃ¤chsten Lauf mit `DIO_CORE_DEBUG` auf DebuggrÃ¶ÃŸe prÃ¼fen.
  Ziel:
  - OrdnergrÃ¶ÃŸe gegen Lauf 63 vergleichen
  - prÃ¼fen, ob die verbleibenden Kernprotokolle fÃ¼r Auswertung reichen
  - bei Bedarf einzelne Protokolle gezielt wieder zuschalten

- [x] Lauf 64 ausgewertet.
  Befund:
  - PnL ca. `+52.14`
  - Drawdown ca. `6.54 %`
  - DebuggrÃ¶ÃŸe ca. `34.29 MB`, deutlich kleiner als Lauf 63
  - Short ca. `+34.57`, Long ca. `+17.57`
  - bestÃ¤tigte Struktur: `54 TP / 0 SL`, ca. `+58.93`
  - offene Strukturhypothese bleibt Hauptlast: ca. `-35.09`

- [x] Stats-Zusammenfassung bei gepuffertem Debug repariert.
  Umsetzung:
  - `TradeStats` hÃ¤lt Outcome-Records zusÃ¤tzlich in einem kleinen
    In-Memory-Cache
  - `trade_stats.json` kann emergente Strukturwerte sofort zusammenfassen
  - `outcome_records.jsonl` bleibt gepuffert und wird nicht schwerer

- [ ] Lauf 65 auf `trade_stats.json`-Emergenzwerte prÃ¼fen.
  Ziel:
  - `kpi_summary.emergent_structure` darf nicht mehr leer/0 sein
  - `trade_equity.csv` weiter fÃ¼r GUI prÃ¼fen
  - DebuggrÃ¶ÃŸe weiter beobachten

- [x] Lauf 65 ausgewertet.
  Befund:
  - PnL ca. `+44.88`
  - Drawdown ca. `9.09 %`
  - DebuggrÃ¶ÃŸe ca. `34.83 MB`
  - `trade_equity.csv` geschrieben mit `371` Equity-Zeilen
  - `trade_stats.json` enthÃ¤lt emergente Strukturwerte korrekt
  - bestÃ¤tigte Struktur: `50 TP / 0 SL`, ca. `+52.21`
  - offene Hypothese getragen: `30 TP / 0 SL`, ca. `+31.89`
  - offene Hypothese reorganisierend: `0 TP / 127 SL`, ca. `-54.68`

- [ ] Reifeschicht fÃ¼r offene Hypothesen weiterentwickeln.
  Ziel:
  - getragene offene Hypothesen nicht bremsen
  - belastete/reorganisierende offene Hypothesen in Nachreifen, Replay,
    Distanzierung und erneute Wahrnehmung fÃ¼hren
  - keine harte Sperre, sondern organische Selbstregulation

- [x] Reifeschicht fÃ¼r offene Hypothesen umgesetzt.
  Umsetzung:
  - `open_hypothesis_bearing_echo`
  - `open_hypothesis_reifung_pressure`
  - `open_hypothesis_reflection_pull`
  - `open_hypothesis_motor_tension`
  - `open_hypothesis_reifung_state`
  - getragen stÃ¤rkt weich, reorganisierend fÃ¼hrt eher zu Replay/Replan

- [ ] Lauf 66 auf offene Hypothesen prÃ¼fen.
  Ziel:
  - Verlustlast von `open_hypothesis_reorganizing` beobachten
  - `open_hypothesis_carried` darf nicht beschÃ¤digt werden
  - VerhÃ¤ltnis aus act / observe / replan prÃ¼fen
  - DebuggrÃ¶ÃŸe weiter beobachten

- [x] Lauf 65 nach Hypothesen-Reifeschicht geprÃ¼ft.
  Befund:
  - PnL ca. `+30.19`
  - Drawdown ca. `11.24 %`
  - bestÃ¤tigte Struktur bleibt stark: `58 TP / 0 SL`, ca. `+58.21`
  - offene reorganisierende Hypothese bleibt stark negativ: ca. `-51.67`
  - normale Strukturlesung deutlich schwÃ¤cher: ca. `+7.59`
  - Reifeschicht wirkt zu breit und zu bremsend

- [x] Crash in Reifeschicht behoben.
  Befund:
  - `open_hypothesis_reifung_state` wurde in der Pre-Action-Kette benutzt,
    bevor die Variable im Funktionsfluss gesetzt war
  Umsetzung:
  - Reifungsberechnung vor die Pre-Action-Entscheidung verschoben
  - doppelte spÃ¤tere Berechnung entfernt
  - Kompilierung sauber

- [x] Zweiten Reihenfolgefehler in Reifeschicht behoben.
  Befund:
  - frÃ¼he Reifungsberechnung griff auf spÃ¤tere Bewusstseinswerte
    `inner_outer_alignment` und `perceptual_distance` zu
  Umsetzung:
  - frÃ¼he Reflexionsspannung nutzt jetzt bereits verfÃ¼gbare Proxies:
    Feldklarheit, Memory-Orientierung und Erfahrungsregulation
  - spÃ¤tere Bewusstseinswerte bleiben weiterhin fÃ¼r spÃ¤tere Regulation aktiv

- [x] `trade_equity.csv` aus Debug-Buffer herausgenommen.
  Umsetzung:
  - Equity-/PnL-Kurve wird sofort geschrieben
  - GUI kann die Datei wÃ¤hrend des Laufs lesen
  - schwere Forschungsdateien bleiben gepuffert

- [ ] Im nÃ¤chsten Lauf prÃ¼fen, ob `trade_equity.csv` live anwÃ¤chst.


- [x] CodeprÃ¼fung nach VS-Code-Absturz durchgefÃ¼hrt.
  Befund:
  - keine Python-Syntaxfehler
  - `debug_lauf_62` ca. `135.57 MB`
  - groÃŸe CSV/JSONL-Dateien sind wahrscheinliche IDE-Belastung
  - Thought-Memory hatte unnÃ¶tige Vollnormalisierung pro Update

- [x] Thought-Memory-Update optimiert.
  Umsetzung:
  - pro Tick inkrementelle Aktualisierung
  - Vollnormalisierung nur beim Schreiben oder deutlichem Ãœberschreiten der
    Limits
  - bestehende `mcm_thought_memory.json` bleibt lesbar

- [x] Debug-Schreiblast gezielt optimieren.
  Ziel:
  - groÃŸe Protokolle nicht dauerhaft maximal schreiben
  - schwere Debugs optional seltener oder nur im Analysemodus schreiben
  - VS-Code-/IDE-Belastung reduzieren
  - Mechanik nicht verÃ¤ndern


- [x] Lauf 62 ausgewertet.
  Befund:
  - PnL ca. `+52.25`
  - Winrate ca. `45.88 %`
  - Attempts sinken gegen Lauf 61: `11300` -> `10275`
  - `family_count`: `768`
  - `family_total_seen`: `1948`
  - Short trÃ¤gt stark: ca. `+38.45`
  - bestÃ¤tigte Struktur: `60 TP / 0 SL`, ca. `+62.75`
  - offene Hypothese bleibt negativ, aber weniger belastend als Lauf 61

- [ ] Lauf 63 auf StabilitÃ¤t der Thought-Families prÃ¼fen.
  Ziel:
  - prÃ¼fen, ob Lauf 62 ein stabiler Sprung oder VorprÃ¤gungseffekt war
  - Top-Familien nach `seen`, Reife und Herkunft auswerten
  - Attempts/Trade beobachten
  - offene Hypothesen prÃ¼fen:
    weniger Last, mehr Reifung oder nur Zufall?


- [x] Thought-Memory-Familienbildung umgesetzt.
  Umsetzung:
  - `mcm_thought_memory.json` bekommt `families`
  - Seeds bekommen `thought_family_id`, `family_key`, `sentence_state`
  - Familien entstehen aus DIO-eigener Syntax, nicht aus menschlichen Labels

- [ ] NÃ¤chsten Lauf auf Thought-Families prÃ¼fen.
  Ziel:
  - `summary.family_count` und `summary.family_total_seen` prÃ¼fen
  - hÃ¤ufigste Familien auswerten
  - prÃ¼fen, ob Familien Wiederholung besser verdichten als Einzel-Seeds
  - offene Hypothesen als Familien-Reifung betrachten

- [x] Lauf 61 ausgewertet.
  Befund:
  - PnL ca. `+29.32`
  - `mcm_thought_memory.json` wurde geschrieben
  - Thought-Memory ist sofort bei `2048` Seeds
  - `total_seen` ca. `2179`, also viele Einzelgedanken mit wenig Wiederholung
  - Short trÃ¤gt stÃ¤rker als Long:
    Short ca. `+19.73`, Long ca. `+9.58`
  - `confirmed_structural_interpretation` bleibt sehr stark:
    `49 TP / 0 SL`, ca. `+50.94`
  - `open_structural_hypothesis` bleibt Hauptlast:
    `24 TP / 137 SL`, ca. `-33.66`

- [ ] Thought-Memory-Familienbildung prÃ¼fen.
  Ziel:
  - nicht nur einzelne `thought_seed_id` speichern
  - Ã¤hnliche Seeds weich zu Gedankenfamilien verdichten
  - Fragmentierung senken
  - wiederkehrende innere Themen sichtbar machen
  - keine harte Regel, sondern organische Verdichtung der eigenen Syntax


- [ ] Sprachentwicklung als Bindeglied weiter ausarbeiten.
  Ziel:
  - DIOs eigene Syntax nicht nur als Label, sondern als
    Wahrnehmungs-/Handlungsbindung verstehen
  - prÃ¼fen, wie Formzeichen und Thought-Seeds zu Relationen werden kÃ¶nnen
  - spÃ¤ter eigene Satzstrukturen in DIO-Syntax ermÃ¶glichen
  - menschliche Sprache nur als Ãœbersetzung/Debug verwenden


- [ ] Eigene DIO-Syntax konsequent durch das System prÃ¼fen.
  Ziel:
  - menschliche Begriffe nur als Debug-/Ãœbersetzungslabel verwenden
  - interne Entscheidungen stÃ¤rker Ã¼ber Formzeichen, Thought-Seeds,
    FeldzustÃ¤nde und eigene Verdichtungen laufen lassen
  - prÃ¼fen, wo noch menschliche Kategorien als innere Wahrheit wirken kÃ¶nnten
  - spÃ¤tere Satzbildung als Relation zwischen DIO-eigenen Zeichen denken,
    nicht als kopierte Menschensprache


- [x] Lauf 60 ausgewertet.
  Befund:
  - PnL ca. `+36.68`
  - Short trÃ¤gt stÃ¤rker als Long:
    Long ca. `+9.76`, Short ca. `+26.92`
  - `confirmed_structural_interpretation` bleibt sehr stark:
    `53 TP / 0 SL`, ca. `+54.57`
  - `open_structural_hypothesis` bleibt Hauptlast:
    `28 TP / 152 SL`, ca. `-35.26`
  - Thought-Memory wurde in Lauf 60 noch nicht geschrieben, weil der Lauf vor
    dem Einbau gestartet war

- [ ] NÃ¤chsten Lauf mit neuem Thought-Memory und Direction-Profil prÃ¼fen.
  Ziel:
  - `bot_memory/mcm_thought_memory.json` muss entstehen
  - `kpi_summary.direction_profile` muss in `trade_stats.json` sichtbar sein
  - Long/Short nicht als Regel, sondern als Richtungserleben auswerten
  - offene Strukturhypothesen auf Reifung statt reflexhaftes Handeln prÃ¼fen


- [ ] RichtungsprÃ¤ferenz spÃ¤ter als WahrnehmungsrÃ¼ckfÃ¼hrung prÃ¼fen.
  Ziel:
  - `direction_profile` nicht als Regel verwenden
  - Long/Short/Gemischt als innere Charakteristik lesen
  - mÃ¶gliche spÃ¤tere Werte:
    `direction_pull`, `direction_bearing_quality`, `direction_stress`,
    `direction_trust`, `direction_blindness`
  - Frage:
    "Warum zieht mein Feld eher in diese Richtung, und was macht diese
    Richtung mit meiner Innenlage?"


- [x] Long/Short-Charakteristik als Counter ergÃ¤nzt.
  Umsetzung:
  - Trades, TP/SL und PnL werden je Richtung gezÃ¤hlt
  - Entry-Versuche, submitted und filled werden je Richtung gezÃ¤hlt
  - Ausgabe in `trade_stats.json` und `kpi_summary.direction_profile`

- [ ] NÃ¤chsten Lauf auf Richtungsprofil prÃ¼fen.
  Ziel:
  - `long_trade_share` vs. `short_trade_share` prÃ¼fen
  - `long_attempt_share` vs. `short_attempt_share` prÃ¼fen
  - Long-/Short-Winrate und Long-/Short-PnL auswerten
  - unterscheiden, ob DIO eine Richtung nur sucht oder ob sie auch tragfÃ¤hig
    gefÃ¼llt und abgeschlossen wird


- [x] Separates Thought-Memory angelegt.
  Umsetzung:
  - neuer Pfad `bot_memory/mcm_thought_memory.json`
  - getrennt von `memory_state.json` und `form_symbol_memory.json`
  - speichert innere Gedankenkeime verdichtet nach Seed-ID
  - kein harter Eingriff in Motorik oder Entry-Entscheidung

- [ ] NÃ¤chsten Lauf auf Thought-Memory prÃ¼fen.
  Ziel:
  - prÃ¼fen, ob `mcm_thought_memory.json` geschrieben wird
  - `summary.seed_count` und `summary.total_seen` beobachten
  - prÃ¼fen, ob `borrowed_reinterpretation_needed`,
    `reinterpretation_memory_trace`, `replay_memory_trace`,
    `own_field_binding_developing` sichtbar werden
  - klÃ¤ren, ob diese Spur spÃ¤ter nur Diagnose bleibt oder weich in
    Thought-Seed-Reifung, Replay und Fokus zurÃ¼ckgefÃ¼hrt wird


# Aktiver Fokus

- [x] `_gui.py` vereinfacht und neu angeordnet.
  - Nur noch Markt-/Chartfenster, Candle State, Trade Stats/KPI,
    Backtest-Prozent und Equity-Kurve.
  - ZusÃ¤tzliche Diagnose-, Memory-, Innenwelt- und Neuronenpanels entfernt.
  - `_gui.py` nutzt automatisch den neuesten `debug/debug_lauf_x`-Ordner.
  - Optionaler Start mit `--debug-run debug_lauf_44`.
  - `py_compile` fÃ¼r `_gui.py` sauber.

- [x] Emergenz als Kernprinzip ergÃ¤nzt.
  - Emergenz wird nicht direkt programmiert.
  - MCM stellt den MÃ¶glichkeitsraum bereit, in dem sich stabile emergente
    Varianz, Strukturdeutung, Reife und Verhalten bilden kÃ¶nnen.
  - Profit/PnL ist nicht Kernziel, sondern mÃ¶gliches Nebenprodukt
    tragfÃ¤higer innerer Organisation.
  - ErgÃ¤nzt in `README.md`, `UMSETZUNGSPLAN.md`,
    `WICHTIG_MECHANIKEN.md` und `AKTUELLER_STAND.md`.

- [x] Markdown-Umlaute korrigiert.
  - `README.md` und `files/*.md` von hÃ¤ufigen `ae/oe/ue`-Schreibweisen
    auf echte UTF-8-Umlaute umgestellt.
  - Code, Variablennamen, technische Keys und Dateinamen bleiben ASCII.

- [x] Erfahrungsbericht zum Bau und Verhalten des DIO/MCM-Systems angelegt.
  - Datei: `docs/04_berichte/ERFAHRUNGSBERICHT_DIO_MCM.md`
  - Zweck: technische Forschungsnotiz Ã¼ber SprÃ¼nge, Verhalten und
    Besonderheiten der nichtklassischen MCM-Programmierung.

- [x] Neurochemische Alias-Schicht bauen.
  Ziel:
  - `neurochemical_state` im Runtime-Ergebnis erzeugen
  - vorhandene Werte als technische Achsen bÃ¼ndeln:
    `dopamine_tone`, `gaba_inhibition`, `noradrenaline_arousal`,
    `acetylcholine_focus`, `serotonin_stability`, `cortisol_load`,
    `endorphin_relief`, `glutamate_activation`
  - zunÃ¤chst Diagnose/Debug, spÃ¤ter weiche Meta-Regulation

- [ ] NÃ¤chsten Lauf mit neurochemischer Diagnose prÃ¼fen.
  Ziel:
  - TP/SL gegen `cortisol_load`, `gaba_inhibition`, `dopamine_tone`,
    `acetylcholine_focus`, `serotonin_stability` und `neurochemical_balance`
    auswerten
  - Regimewechsel nicht mechanisch bewerten, sondern Last/Support lesen
  - Lauf 10 als ersten neurochemischen Referenzlauf nutzen

- [x] Neurochemische Ãœbergaenge aus Lauf 10 vertiefen.
  Ziel:
  - `serotonin_stability -> glutamate_activation` gegen Handlung nÃ¤her
    untersuchen
  - strukturelle Kipp-Momente mit `cortisol_load`, `gaba_inhibition`,
    `zero_point_regulation` und `observe` vergleichen
  - klÃ¤ren, ob DIO aus StabilitÃ¤t aktiviert oder aus Last kippt
  Befund:
  - erster `-2/+2` Kerzenvergleich spricht fÃ¼r zwei Muster:
    Glutamat-Aktivierung aus stabiler Grundlage vs. Cortisol-Kippmoment bei
    Volumen-/Range-Spikes

- [ ] Neues neurochemisches Ãœbergangsprotokoll im nÃ¤chsten Lauf prÃ¼fen.
  Ziel:
  - `mcm_neuro_transition_protocol.csv` auf VollstÃ¤ndigkeit prÃ¼fen
  - Transitionen gegen TP/SL, `observe`, `act_watch`, `act` und
    `zero_point_regulation` lesen
  - klÃ¤ren, ob DIO aus StabilitÃ¤t aktiviert oder unter Last kippt
  Status:
  - Lauf 11 bestÃ¤tigt Protokollausgabe.
  - NÃ¤chster Schritt: Zone-Verlust gegen Non-Zone-Verbesserung auswerten.

- [ ] Zone-PrÃ¤zision gegen TransferfÃ¤higkeit untersuchen.
  Ziel:
  - klÃ¤ren, warum Non-Zone in Lauf 11 besser wurde, Zone aber schwacher
  - `glutamate_activation` bei SL gegen TP vergleichen
  - prÃ¼fen, ob DIO zu viel Aktivierung in eigentlich bekannten Zonen
    zugelassen hat
  Befund:
  - Lauf 11 zeigt Aktivierung ohne ausreichend tragende Reife als Kernrisiko.
  - Non-Zone profitierte leicht von mehr Transfer, Zone verlor
    AuswahlprÃ¤zision.

- [ ] Aktivierungs-TragfÃ¤higkeit als Diagnoseachse vorbereiten.
  Ziel:
  - keine harte Regel bauen
  - `glutamate_activation` gegen `neurochemical_balance`,
    `action_inhibition`, `action_clearance`, `transfer_bearing` und
    `variant_bearing_memory` lesen
  - unterscheiden zwischen reifer Aktivierung und nervlicher Ãœberfeuerung

- [x] Core-Engine WahrnehmungsÃ¼bersetzung entlasten.
  Ziel:
  - prÃ¼fen, ob Chartreize mehrfach als gleichgerichteter Alarm wirken
  - Risiko-/Threat-Achse mit echter RÃ¼ckregulation versehen
  - keine harte Regel, sondern sensorische Habituation und Reizverdichtung
  - DIO soll Form sehen, nicht dauerhaft im Stressmilieu tasten
  Befund:
  - Lauf 11 zeigt fast permanent `stressed` und stark negative
    `mean_risk`-Achse.
  - `visual_form_pressure` ist stark mit mehreren AuÃŸenreizachsen
    gekoppelt.

- [ ] NÃ¤chsten Lauf nach sensorischer Entdoppelung prÃ¼fen.
  Ziel:
  - `self_state=stressed`-Anteil und `mean_risk` vergleichen
  - `mcm_visual_cortex_protocol.csv` auf `sensory_redundancy`,
    `sensory_gate` und `sensory_reality_label` prÃ¼fen
  - klÃ¤ren, ob DIO weniger doppelte Strukturreize und mehr klare
    RealitÃ¤tsform wahrnimmt

- [x] NÃ¤chsten Lauf nach Outcome-Export-Erweiterung prÃ¼fen.
  Ziel:
  - prÃ¼fen, ob `outcome_records.jsonl` jetzt Formfamilienwerte enthÃ¤lt
  - TP/SL gegen `variant_learning_pressure`, `uncertainty_familiarity`,
    `variant_bearing_memory`, `visual_action_uncertainty` auswerten
  - Lauf 8 als Referenz nutzen

- [ ] Regimewechsel-Bewaeltigung aus Lauf 9 vertiefen.
  Ziel:
  - klÃ¤ren, warum Formvertrautheit nicht immer zu Handlungssicherheit wird
  - `memory_compare_load`, `orientation_gap`, `blind_thinking_load`,
    `action_clearance`, `action_inhibition` gegen TP/SL betrachten
  - keine harte Regel ableiten, sondern Reife-/TragfÃ¤higkeitsdiagnostik
    verbessern

- [ ] Sensorische Erfahrungssynchronisation nach Lauf 12/13 prÃ¼fen.
  Ziel:
  - klÃ¤ren, ob alte Memory-Signaturen zur neuen sensorischen Kodierung passen
  - nicht den Speicher lÃ¶schen, sondern Anpassungsdruck sichtbar machen
  - `memory_compare_load`, `sensory_gate`, `visual_form_pressure`,
    `action_inhibition`, `regulated_courage` und PnL-Verlauf gemeinsam lesen

- [ ] Serotonin-Nachhall beim Regimewechsel prÃ¼fen.
  Ziel:
  - erkennen, ob `serotonin_carryover_risk` im Abverkauf steigt
  - prÃ¼fen, ob DIO weiter aus alter StabilitÃ¤tslage handelt
  - `emotional_decoupling` und `reactive_nervous_drive` gegen TP/SL und
    Equity-Bruch lesen

- [x] Selektive Wahrnehmung / perzeptive Regulation als nÃ¤chsten
  Architekturblock vorbereiten.
  Ziel:
  - Wahrnehmungen nicht hart filtern, sondern ihre NÃ¤he zum MCM-Feld weich
    regulieren
  - `perceptual_distance`, `object_contact_depth`, `field_attachment`,
    `release_capacity`, `selective_attention`, `background_containment`,
    `reflective_distance` und `inner_outer_alignment` als Zielachsen prÃ¼fen
  - DIO soll Reize sehen, vertiefen oder ablegen kÃ¶nnen, ohne jeden Eindruck
    vollstÃ¤ndig zu durchleben

- [x] Bewusste Wahrnehmung / innere Reizwirkungsanalyse diagnostisch bauen.
  Ziel:
  - nicht nur Reize dÃ¤mpfen, sondern ihre Wirkung im MCM-Feld bewusst lesbar
    machen
  - prÃ¼fen: Was hat der Ã¤uÃŸere Reiz mit dem MCM-Feld gemacht?
  - Zielachsen: `conscious_perception_state`, `stimulus_field_effect`,
    `inner_impact_trace`, `perceived_field_change`, `felt_afterimage`,
    `object_release_state`, `inner_outer_reflection`
  - Grundlage fÃ¼r echte Reflexion und regulatorische Steuerung schaffen

- [ ] Lauf 17 mit bewusster Wahrnehmung auswerten.
  Ziel:
  - `conscious_perception_state`, `field_attachment`, `perceptual_distance`,
    `release_capacity` und `inner_outer_alignment` gegen TP/SL,
    Regimewechsel und Equity-Verlauf lesen
  - prÃ¼fen, ob DIO im Abverkauf Ã¼berkoppelt, reflektiv Abstand findet oder
    Reize loslassen kann
  - danach erst entscheiden, ob eine weiche Regulation auf diese Achsen
    aufgebaut wird

- [x] Bewusste Wahrnehmungslabels feiner kalibrieren.
  Befund aus neuem `debug_lauf_1`:
  - alle Protokollzeilen stehen auf `open_perception`
  - alle Release-ZustÃ¤nde stehen auf `holding`
  - numerische Achsen bewegen sich, aber die Labels unterscheiden noch nicht
    fein genug
  Ziel:
  - keine harte Handelsregel
  - Labels dynamischer aus relativer Innenlage bilden
  - `object_contact`, `reflective_check`, `overcoupled_field` und
    `release_ready` natÃ¼rlich sichtbar machen

- [x] Lauf 2 mit innerer Haltung auswerten.
  Ziel:
  - prÃ¼fen, ob `conscious_perception_state` und `inner_posture_state` nun
    streuen
  - `curious`, `excited`, `overstimulated`, `tired`, `calm` und `reflective`
    gegen TP/SL, Equity-Bruch und Regimewechsel lesen
  - keine harte Regel ableiten, sondern erst prÃ¼fen, welche inneren
    Haltungen tragfÃ¤hig oder belastend werden

- [x] Diffuse Offenheit weich weiterentwickeln.
  Befund aus Lauf 2:
  - `uncertain_open` und `open_perception` waren bei Trades negativ
  - benannte Aktivierung wie `excited`, `curious` oder `overcoupled_field`
    war nicht automatisch schlecht
  Ziel:
  - keine harte Blockade auf `uncertain_open`
  - DIO soll diffuse Offenheit eher in Beobachtung, Objektkontakt,
    Reflexion oder Loslassen Ã¼berfÃ¼hren
  - prÃ¼fen, ob dadurch weniger blinde Handlungen entstehen

- [ ] Lauf 3 mit diffuser Offenheitsreifung prÃ¼fen.
  Ziel:
  - `diffuse_open_development_pressure` und `posture_development_hint` gegen
    TP/SL und Equity-Verlauf lesen
  - prÃ¼fen, ob `uncertain_open`-Trades sinken
  - prÃ¼fen, ob gute Aktivierung (`curious`, `excited`, tragendes
    `overcoupled_field`) nicht erstickt wird

- [ ] Wache Anstrengung statt Gleichgueltigkeit bauen.
  Befund aus Lauf 3:
  - Trades sanken, PnL brach dennoch stark ein
  - Zone war positiv, Non-Zone massiv negativ
  - `uncertain_open` sank, aber Schaden wanderte in schwache
    `object_contact`-/Non-Zone-Handlungen
  Ziel:
  - kein harter Non-Zone-Block
  - `diffuse_open_development_pressure` nicht pauschal Courage senken lassen
  - `engaged_effort` / wache Anstrengung als Gegenpol zu Unterspannung
    prÃ¼fen
  - Non-Zone bei niedriger TragfÃ¤higkeit eher in Beobachtungslernen,
    Reflexion oder Loslassen Ã¼berfÃ¼hren

- [x] Erfahrungspaket-Feedback / positive Stimulation bauen.
  Ziel:
  - kein `TP = gut` / `SL = schlecht`
  - gesamtes Paket bewerten: Struktur, Innenlage, Wahrnehmung, Haltung,
    Handlung, Risiko, Ergebnis, Wiederholbarkeit
  - gute Prozessleistung positiv stimulieren
  - schlechte PaketqualitÃ¤t als Reorganisationssignal nutzen
  - auch Abverkauf positiv bewerten kÃ¶nnen, wenn Entscheidung und Prozess
    tragfÃ¤hig waren
  - Grundlage fÃ¼r `engaged_effort` als positiv getragene Wachheit schaffen
  Status:
  - umgesetzt in `build_experience_packet_feedback`
  - sichtbar in `last_outcome_decomposition` und `outcome_records.jsonl`
  - in Episode-/Ã„hnlichkeitsachsen des Erfahrungsraums angebunden
  - nÃ¤chster Lauf prÃ¼ft, ob positive Prozesspakete und Reorganisationspakete
    sinnvoll streuen

- [ ] Non-Zone als Beobachtungs-/Lernraum weiter reifen lassen.
  Ziel:
  - keine harte Non-Zone-Blockade
  - Non-Zone eher als unreifer Erfahrungsraum behandeln
  - prÃ¼fen, ob Non-Zone-Schaden sinkt, ohne Zone-Handlung zu ersticken

- [x] Erfahrungspaket-Label nach Lauf 4 feiner kalibrieren.
  Befund:
  - `experience_packet_feedback` funktioniert technisch
  - fast alle Trades landen aber in `mixed_packet`
  - gute Prozesspakete werden noch nicht als `constructive_packet` sichtbar
  Ziel:
  - keine Handelsregel bauen
  - nur die Selbstwahrnehmung des Pakets feiner benennen
  - konstruktive Pakete, Reorganisationspakete und Neugierpakete besser
    unterscheidbar machen
  Status:
  - Labelschwellen angepasst
  - konstruktive Pakete kÃ¶nnen jetzt Ã¼ber Prozessreward +
    begrenzten Reorganisationsdruck sichtbar werden

- [x] `engaged_effort` / wache Anstrengung bauen.
  Ziel:
  - positive ProzessqualitÃ¤t in Wachheit statt Gleichgueltigkeit Ã¼bersetzen
  - Non-Zone nicht blockieren, sondern bei niedriger TragfÃ¤higkeit eher in
    Beobachtung, Reifung oder Reorganisation fÃ¼hren
  - unterscheiden: reife Aktivierung, blinde Aktivierung, Unterspannung,
    neugieriges Beobachten
  Status:
  - `engaged_effort`, `effort_state`, `effort_learning_pull` und
    `effort_reorganization_pressure` umgesetzt
  - sichtbar in Meta-Regulation, Field-Protokoll und Outcome-Records

- [x] Lauf 5 mit `engaged_effort` prÃ¼fen.
  Ziel:
  - prÃ¼fen, ob `constructive_packet` jetzt sichtbar wird
  - `effort_state` gegen TP/SL, Zone/Non-Zone und PnL lesen
  - besonders `underengaged_reorganize` gegen Non-Zone-Verluste prÃ¼fen
  Status:
  - erledigt
  - `constructive_packet` wurde sichtbar und war klar positiv
  - `bearing_packet` war falsch positiv benannt und wurde nachkalibriert
  - `underengaged_reorganize` war noch nicht sichtbar; Sensitivitaet erhoeht

- [x] Lauf 6 nach Paket-/Effort-Nachkalibrierung prÃ¼fen.
  Ziel:
  - weniger falsche `bearing_packet`
  - mehr sinnvolle `reorganize_packet`
  - `underengaged_reorganize` sichtbar machen
  - Non-Zone-Verluste gegen Beobachtung/Replan lesen
  Status:
  - `bearing_packet` ist verschwunden
  - `constructive_packet` bleibt klar positiv
  - `reorganize_packet` ist klar sichtbar, aber noch zu spÃ¤t
  - `underengaged_reorganize` ist sichtbar, aber zu selten

- [x] Reorganisationswahrnehmung frÃ¼her in Pre-Action Ã¼bertragen.
  Ziel:
  - keine Blockade
  - nicht mehr handeln
  - schwache PaketqualitÃ¤t und geringe TragfÃ¤higkeit vor der Handlung eher
    in `observe`, `act_watch` oder `replan` Ã¼berfÃ¼hren
  - Non-Zone-Verluste reduzieren, ohne konstruktive Zone-Pakete zu ersticken
  Status:
  - `pre_action_reorganization_pressure` umgesetzt
  - `pre_action_context_selectivity` umgesetzt
  - sichtbar in Field-/Memory-Protokoll und Outcome-Records

- [x] Lauf 7 nach Pre-Action-Reorganisation prÃ¼fen.
  Ziel:
  - `pre_action_reorganization_observe` und
    `pre_action_reorganization_replan` zaehlen
  - Non-Zone-Schaden vergleichen
  - prÃ¼fen, ob konstruktive Zone-Pakete erhalten bleiben
  Status:
  - erledigt
  - konstruktive Pakete bleiben sehr sauber positiv
  - Pre-Action-Reorganisation wird im Feld sichtbar, greift aber nur selten
    als konkreter Observe/Replan-Grund
  - Achse trennt Zone/Non-Zone noch nicht gut genug

- [x] Pre-Action-Reorganisation strukturgenauer machen.
  Ziel:
  - `pre_action_reorganization_pressure` stÃ¤rker an aktuelle
    StrukturqualitÃ¤t, Kontextvertrauen und Feldsupport koppeln
  - `pre_action_context_selectivity` fÃ¼r gute Zone-Kontexte erhÃ¶hen
  - nicht pauschal vorsichtig werden
  - schwache Non-Zone-Kontexte frÃ¼her in Beobachtung/Replan fÃ¼hren
  Status:
  - umgesetzt
  - `structure_quality` und `context_confidence` in Pre-Action-Druck und
    Kontextselektivitaet integriert

- [x] Lauf 8 nach strukturgenauer Pre-Action-Reorganisation prÃ¼fen.
  Ziel:
  - Zone/Non-Zone-Trennung der Pre-Action-Achsen vergleichen
  - `pre_action_reorganization_observe/replan` zaehlen
  - konstruktive Pakete und Non-Zone-Schaden gegen Lauf 7 vergleichen
  Status:
  - erledigt
  - konstruktive Pakete bleiben sauber positiv
  - Pre-Action-Achsen trennen ausgefÃ¼hrte Zone/Non-Zone noch kaum
  - nÃ¤chster Schritt ist strategische Fensterwahrnehmung statt weiteres
    Drehen an derselben Pre-Action-Achse

- [x] Strategische Fensterwahrnehmung / Preisbereich-Hypothesen vorbereiten.
  Ziel:
  - grÃ¶ÃŸeres Fenster betrachten
  - zurÃ¼ckschauen, zoomen, Replay-Spuren bilden
  - auffÃ¤llige Preisbereiche als MCM-Hypothesen erkennen
  - keine FVG-Regel einpflanzen
  - nicht bestimmen, wo DIO handeln soll
  - Druck als Raum lesen, nicht als Handlungsbefehl
  - DIO die FÃ¤higkeit geben, aus Vergangenheit, Wahrnehmung und innerem Feld
    eigene Zukunftshypothesen zu bilden
  - spÃ¤ter wartende Order-Intention aus Bereich + Memory + Innenlage bilden
  Status:
  - diagnostisch umgesetzt
  - `mcm_strategic_window_protocol.csv` schreibt Lookback-, Zoom-, Replay-
    und Bereichshypothesen
  - noch keine harte Orderintegration

- [x] Begrenztes RÃ¼ckblickfenster fÃ¼r strategische Wahrnehmung definieren.
  Ziel:
  - kein grenzenloses ZurÃ¼ckschauen
  - Lookback-Budget, Zoom-Budget und Replay-Budget diagnostisch sichtbar
    machen
  - alte Struktur mit Verfall / Carryover-Risiko versehen
  - DIO soll Vergangenheit nutzen, aber nicht in alter Struktur hÃ¤ngen
  Status:
  - diagnostisch umgesetzt
  - Lookback wird durch Last, Fokus und StabilitÃ¤t budgetiert
  - `old_structure_carryover_risk` macht alte Strukturbindung sichtbar

- [x] Lauf 1 nach strategischer Fensterdiagnose prÃ¼fen.
  Ziel:
  - `mcm_strategic_window_protocol.csv` lesen
  - prÃ¼fen, ob Bereichshypothesen vor guten/schlechten Trades anders wirken
  - sehen, ob Regimewechsel eher `area_needs_zoom`, `area_releasing` oder
    `bearing_area_hypothesis` erzeugt
  - noch keine Handelsregel daraus bauen
  Status:
  - erledigt
  - frischer Memory-Lauf stark negativ
  - alle ausgefÃ¼hrten Trades im Zone-Bucket
  - strategische Order-Intention noch schwach
  - kompletter `strategic_window_state` fehlt noch im Attempt-Kontext

- [ ] Strategische Fensterwahrnehmung in Attempt-/Outcome-Kontext vollstÃ¤ndig Ã¼bergeben.
  Ziel:
  - `strategic_window_state` nicht nur reduziert in `meta_regulation_state`
    speichern
  - komplette Bereichsachsen in `attempt_records.jsonl` und spÃ¤teren
    Outcome-Auswertungen sichtbar machen
  - Analyse von TP/SL gegen Bereichshypothesen sauberer machen

- [ ] Strategische Fensterwahrnehmung weich an Pre-Action-Reife koppeln.
  Ziel:
  - keine harte Handelsregel
  - niedrige `area_order_intention` + niedriger Memory-Pull + geringe
    strategische Geduld als Zoom-/Observe-/Replay-Reifespur verwenden
  - Verdichtung nicht automatisch als Handlungsreife lesen
  - DIO soll Bereich sehen, halten, verwerfen oder spÃ¤ter nutzen kÃ¶nnen

- [x] Aktiven MCM-Kontakt diagnostisch bauen.
  Ziel:
  - MCM nicht nur als Empfaenger Ã¤uÃŸerer Reize behandeln
  - aktive Kontaktbahn aus Wahrnehmungsobjekt, Interesse, Resonanz,
    Innen-AuÃŸen-KohÃ¤renz, Ãœberkopplung, Loslassen und Vertiefung sichtbar
    machen
  - keine harte Order-Regel
  - DIO die FÃ¤higkeit geben, eine Wahrnehmung nÃ¤her an sich heranzulassen,
    Abstand zu nehmen, zu replayen, zu beobachten oder zu vertiefen
  Technische Zielachsen:
  - `active_mcm_contact_state`
  - `contact_interest`
  - `contact_resonance_probe`
  - `outer_inner_coherence`
  - `inner_change_from_contact`
  - `contact_carrying_quality`
  - `contact_overcoupling_risk`
  - `contact_release_readiness`
  - `contact_selected_depth`
  - `contact_posture`
  Status:
  - umgesetzt in `MCM_Brain_Modell.py`
  - `build_active_mcm_contact_state(...)` erzeugt Kontaktlage rein
    diagnostisch
  - keine harte Orderwirkung

- [x] Aktiven MCM-Kontakt in Debug/Outcome sichtbar machen.
  Ziel:
  - eigenes Protokoll, z.B. `mcm_active_contact_protocol.csv`
  - Kontaktzustand in Runtime-Snapshot und Attempt-/Outcome-Kontext aufnehmen
  - spÃ¤ter prÃ¼fen, ob gute Trades eher aus kohÃ¤rentem Kontakt entstehen
    und schlechte Trades eher aus Ãœberkopplung, geringer Distanz oder
    fehlender LoslassfÃ¤higkeit
  Status:
  - `mcm_active_contact_protocol.csv` ergÃ¤nzt
  - Runtime-Snapshot, Attempt-Kontext und Outcome-Kontext erweitert
  - Smoke-Test erfolgreich

- [x] Aktiven MCM-Kontakt im nÃ¤chsten Lauf auswerten.
  Ziel:
  - Verteilung von `contact_posture` lesen
  - TP/SL gegen `contact_overcoupling_risk`, `outer_inner_coherence`,
    `contact_release_readiness` und `contact_carrying_quality` vergleichen
  - prÃ¼fen, ob schlechte Entscheidungen eher aus Ãœberkopplung oder aus
    zu geringer Kontakt-Tiefe entstehen
  - danach erst Ã¼ber weiche Kopplung an Reflexion/Pre-Action-Reife sprechen
  Status:
  - Lauf `debug_lauf_2` ausgewertet
  - Kontaktprotokoll funktioniert
  - fast alle Kontaktlagen bleiben `background_scan`
  - Kontaktwerte unterscheiden sich, aber Haltungssprache ist noch zu grob
  - High-Struktur trÃ¤gt, Mid/Low erzeugt den Hauptschaden

- [x] Aktive MCM-Kontaktlabels feiner kalibrieren.
  Ziel:
  - Kontaktlagen nicht als starre Schwelle verstehen
  - relative Lage zwischen KohÃ¤renz, Ãœberkopplung, Loslassen, Interesse und
    TragfÃ¤higkeit stÃ¤rker auswerten
  - `background_scan` darf nicht fast alle ZustÃ¤nde verschlucken
  - `curious_touch`, `reflective_contact`, `overcoupled_touch`,
    `release_contact`, `deepening_contact` und `resonant_contact` natÃ¼rlich
    sichtbarer machen
  - keine direkte Orderregel bauen
  Status:
  - umgesetzt
  - Haltungsauswahl nutzt jetzt relative Scores statt nur harte
    Einzelschwellen
  - zusÃ¤tzliche Diagnosewerte:
    `contact_salience`, `overcoupled_touch_score`, `release_contact_score`,
    `deepening_contact_score`, `resonant_contact_score`,
    `reflective_contact_score`, `curious_touch_score`
  - Smoke-Test:
    - tragender Kontakt -> `resonant_contact`
    - aktionsnaher Kontakt mit geringer LoslassfÃ¤higkeit ->
      `overcoupled_touch`

- [ ] KontaktqualitÃ¤t gegen Mid/Low-Verlustzonen prÃ¼fen.
  Ziel:
  - untersuchen, ob Mid/Low-Trades vor Handlung niedrige
    `contact_carrying_quality`, niedrige `contact_release_readiness`,
    geringe `outer_inner_coherence` oder hohe `contact_overcoupling_risk`
    zeigen
  - daraus eine weiche Reifespur fÃ¼r Observe/Zoom/Replay ableiten
  - keine harte Verbotslogik
  Status:
  - Lauf `debug_lauf_3` geprÃ¼ft
  - Kontaktlabels streuen jetzt sauber
  - `background_scan` verschluckt die ZustÃ¤nde nicht mehr
  - Low-Struktur bleibt Hauptverlustzone
  - `deepening_contact` ist im Trade-Kontext deutlich negativ
  - `resonant_contact` ist leicht positiv, aber nicht automatisch
    tradefÃ¤hig
  - Lauf 4 zeigt: Hauptschaden liegt in Mid-Struktur; Kontakt-Reife muss
    stÃ¤rker mit Regime-/Kontext-Reife gekoppelt werden
  - Lauf 5 zeigt: Kontakt-/Kontext-Reife allein trennt TP/SL noch nicht
    stark genug; visuelle Erdung der MCM-Reaktion wurde als nÃ¤chster
    Mechanikschritt umgesetzt

- [x] Kontakt-Reife weich in Pre-Action-Regulation und Kontext-Reife sichtbar machen.
  Ziel:
  - keine harte Low-Sperre
  - schwache Struktur + `deepening_contact` / `curious_touch` /
    `overcoupled_touch` als Reifespur fÃ¼r Beobachtung, Replay,
    Abstand oder weitere Objektbildung interpretieren
  - KontaktnÃ¤he nicht automatisch als Handlungsreife lesen
  - DIO die FÃ¤higkeit geben, zwischen "ich fÃ¼hle Kontakt" und
    "dieser Kontakt trÃ¤gt Handlung" zu unterscheiden
  Umsetzung:
  - neue Diagnoseachsen:
    `contact_action_maturity`, `contact_bearing_gap`,
    `contact_impulse_vs_bearing`, `contact_learning_need`,
    `contact_reality_check`
  - Kontextkopplung:
    `contact_regime_mismatch`, `contact_stability_carryover`,
    `contact_context_maturity`, `contact_context_reframe_need`
  - nur Diagnose/Protokollierung, kein hartes Eingreifen in die
    Handelsentscheidung

- [x] Visual Grounding als visuelles Sinnesorgan umsetzen.
  Ziel:
  - innere MCM-Resonanz an Ã¤uÃŸere Formbindung koppeln
  - Formresonanz ohne Objektbindung sichtbar machen
  - DIO mehr Sehkraft geben, ohne menschliche Pattern-Regeln einzubauen
  Umsetzung:
  - neue Werte:
    `visual_object_binding`, `visual_grounding_strength`,
    `visual_resonance_unbound`, `visual_grounding_gap`,
    `visual_grounding_need`, `visual_rational_observation_support`,
    `visual_grounding_state`
  - weiche Wirkung auf Beobachtung, Replan und visuelle
    Handlungsunsicherheit
  - keine harte Orderblockade

- [x] Semantisches Forminhalt-Paket fÃ¼r die Formsprache umsetzen.
  Ziel:
  - DIOs eigene Formzeichen in Bedeutungsschichten verdichten
  - sichtbar machen, ob eine Form eher Spur, Objekt, Lernraum, Reflexion,
    zusammengesetzte Form oder HandlungsnÃ¤he ist
  - keine menschlichen Chart-Labels erzwingen
  - keine harte Handlungsregel einbauen
  Umsetzung:
  - neue Werte:
    `form_symbol_semantic_density`,
    `form_symbol_semantic_compression`,
    `form_symbol_semantic_coherence`,
    `form_symbol_semantic_learning_need`,
    `form_symbol_semantic_action_nearness`,
    `form_symbol_semantic_primary_layer`,
    `form_symbol_semantic_layer_count`,
    `form_symbol_semantic_packet_state`,
    `form_symbol_semantic_profile`
  - Runtime-State, Formsymbol-Protokoll und Outcome-Kontext erweitert

- [x] Evolutionaere Kontaktreife fÃ¼r Formzeichen umsetzen.
  Ziel:
  - nicht die Form als gut/schlecht bewerten
  - den Umgang mit der Form lernen
  - konsequenzbasiertes Feedback auf das MCM-Feld als Lernkreis speichern
  - belastende Konsequenzspur, Nutzen, Vorsicht und Reife als
    Erfahrungsspuren speichern
  - keine harte Sperre, keine mechanische Low-Regel
  Umsetzung:
  - neue Speicher-/Runtime-Werte:
    `form_symbol_contact_maturity`,
    `form_symbol_contact_utility`,
    `form_symbol_contact_pain_memory`,
    `form_symbol_contact_carefulness`,
    `form_symbol_contact_burden_evidence`,
    `form_symbol_contact_utility_evidence`,
    `form_symbol_contact_learning_state`
  - neue Outcome-Samples:
    `contact_maturity_sample`,
    `contact_utility_sample`,
    `contact_pain_sample`,
    `contact_carefulness_sample`,
    `contact_learning_state`
  - weich in Entwicklung, Beobachtung, Reframing, Caution und
    HandlungstragfÃ¤higkeit gekoppelt

- [x] Kontaktreife nach Lauf 8 verstÃ¤rkt.
  Ziel:
  - Konsequenzspur aus wiederholtem Kontakt lauter machen
  - nicht nur den letzten Trade bewerten
  - Belastungs-Evidenz und Nutzen-Evidenz als lÃ¤nger wirkende Spuren nutzen
  - `burdened_contact`, `careful_contact`, `maturing_contact` und
    `constructive_contact` natÃ¼rlicher sichtbar machen
  Umsetzung:
  - gespeicherte Kontakt-Evidenz fliesst in Beobachtung, Reframing und
    HandlungstragfÃ¤higkeit ein
  - belastende Kontakte senken impulsnahe Handlung weich
  - tragende Kontakte kÃ¶nnen Handlung weich stuetzen
  - keine harte Sperre und keine mechanische Strukturregel

- [x] Kontaktreife mit strategischer Orderbereich-Wahl koppeln.
  Ziel:
  - DIO darf den Entry weich aus dem RÃ¼ckblick heraus verschieben
  - impulsnaher Entry bleibt als Koerperreflex erhalten
  - strategischer Bereich mischt sich nur bei tragender Fensterwahrnehmung
    und passender Kontaktlage dazu
  Umsetzung:
  - `entry_mode`
  - `impulse_entry_price`
  - `strategic_entry_price`
  - `strategic_entry_weight`
  - `strategic_entry_fit`
  - `strategic_area_focus_id`
  - `strategic_area_price_low`
  - `strategic_area_price_high`

- [x] Zeitfeld fÃ¼r strategische Bereiche umsetzen.
  Ziel:
  - Bereiche nicht nur als Preisraum, sondern als Ereignis im Zeitfeld lesen
  - alte Bereiche als Nachhall/Erinnerung von handlungsnahen Bereichen
    unterscheiden
  - Bereichsmotorik organischer machen
  Umsetzung:
  - `area_temporal_distance`
  - `area_temporal_relevance`
  - `area_recency`
  - `area_decay`
  - `area_afterimage`
  - `area_present_contact`
  - `area_action_timing_fit`

- [ ] Mehrdimensionale Wahrnehmungsachsen diagnostisch bauen.
  Ziel:
  - Reality-Tagging als Teil eines grÃ¶ÃŸeren Achsensystems behandeln
  - aktuelle AuÃŸenwelt, Nachhall, Erinnerung, gelerntes Wissen, Replay,
    Hypothese und Erwartung unterscheiden
  - Memory und Wissen nicht automatisch als Gegenwart behandeln
  - DIO erkennt, ob eine Information jetzt realen Kontakt hat oder nur aus
    vergangener/wieder aktivierter Energie wirkt
  - Wahrnehmungen raeumlich verorten: nah, fern, Vordergrund, Hintergrund,
    Feldzentrum, Rand, Memory-Raum, Hypothesenraum
  MÃ¶gliche Achsen:
  - `perception_source`
  - `source_temporal_layer`
  - `present_world_binding`
  - `memory_reality_distance`
  - `perceptual_space_axis`
  - `perceptual_depth`
  - `field_center_distance`
  - `foreground_binding`
  - `background_afterimage`
  - `learned_knowledge_weight`
  - `afterimage_pressure`
  - `replay_reality_gap`
  - `hypothesis_reality_gap`
  - `source_confusion_load`

- [ ] Zeitliche KohÃ¤renz / WahrnehmungskontinuitÃ¤t bauen.
  Ziel:
  - DIO soll nicht jeden Moment als komplett neu erleben
  - wiederkehrende, fortgesetzte, nachhallende und veraltete Wahrnehmungen
    unterscheidbar machen
  - keine feste Streckenkarte, sondern zeitliche Quellenbindung im MCM-Feld
  - verhindern, dass DIO denselben Kontakt wie ein dementer Organismus immer
    wieder als neues Ereignis findet
  MÃ¶gliche Achsen:
  - `temporal_continuity`
  - `temporal_source_binding`
  - `temporal_recurrence`
  - `temporal_novelty`
  - `temporal_afterimage`
  - `temporal_decay`
  - `temporal_context_depth`
  - `temporal_self_consistency`
  - `perception_sequence_coherence`
  - `memory_time_distance`
  Status:
  - im `UMSETZUNGSPLAN.md` als Abschnitt 18.5 aufgenommen
  - erste Runtime-Mechanik umgesetzt:
    `build_temporal_coherence_state` bildet zeitliche Identitaet,
    Fortsetzung, Wiederkehr, Neuheit, Nachhall und Zeitdistanz
  - Feldentscheidungsprotokoll, Memory-/Thinking-Protokoll und
    Outcome-Records schreiben die neuen Werte mit
  - `active_context_trace` kann jetzt ersatzweise aus zeitlicher
    Wahrnehmung entstehen, wenn kein innerer Cluster aktiv ist
  - nÃ¤chster Schritt: Backtest-Lauf auswerten und prÃ¼fen, ob
    `active_context_activation` nicht mehr leer bleibt und ob DIO weniger
    momenthaft wirkt

- [ ] Gedanken-Energieform diagnostisch vorbereiten.
  Ziel:
  - Gedanken nicht nur als Entscheidungstext, sondern als gerichteten
    Energieverlauf im MCM-Feld lesen
  - lange Gedanken als gedehnte/sparsame/kohÃ¤rent gerichtete Energie
    unterscheidbar machen
  - Rumination, Planung, Erwartung und Nachhall als unterschiedliche
    Zeitstraenge sichtbar machen
  MÃ¶gliche Anknuepfung:
  - `thought_state`
  - `rumination_depth`
  - `inner_time_scale`
  - `thought_alignment`
  - `thought_inertia`
  - `thought_settlement`

- [ ] Hypothesenraum / Reorganisation nach MCM-Abhandlungen D bis G.1 vorbereiten.
  Ziel:
  - MCM-Theorie nicht als Regelwerk, sondern als organische Zielmechanik
    nutzen
  - mehrere mÃ¶gliche Entwicklungszweige halten, ohne sie mit Gegenwart zu
    verwechseln
  - lokale Ãœberlast nicht nur als Fehler, sondern auch als mÃ¶glichen
    Reorganisationsmoment lesen
  MÃ¶gliche Achsen:
  - `hypothesis_branch_state`
  - `branch_stability`
  - `branch_attractor_pull`
  - `hypothesis_reality_gap`
  - `field_reorganization_state`
  - `reorganization_threshold`
  - `higher_order_coupling`

- [ ] Metaregulator-Schicht aus MCM Block S vorbereiten.
  Ziel:
  - Regler zweiter Ordnung fÃ¼r DIO sichtbar machen
  - nicht nur Feldlage messen, sondern wie DIO diese Lage verarbeitet
  - direkte BrÃ¼cke zu selbstregulativer Erfahrungsorganisation
  MÃ¶gliche Achsen:
  - `return_strength`
  - `integration_capacity`
  - `variance_regulation`
  - `load_tolerance`
  - `impulse_control`
  - `frustration_tolerance`
  - `protective_distance_regulation`
  - `self_reflection_regulator`
  - `distance_regulation`
  Status:
  - Diagnose in Runtime, Feldentscheidungsprotokoll,
    Memory-/Thinking-Protokoll und Outcome-Records umgesetzt
  - nÃ¤chster Schritt: Backtest-Lauf auswerten und prÃ¼fen, ob die Werte
    Regimewechsel, Ãœberkopplung, Impulsdruck und RÃ¼ckkehrkraft sinnvoll
    sichtbar machen
  - noch keine harte Verhaltenskopplung eingebaut
  - Unterbewusstsein / bewusster Arbeitsraum als Wahrnehmungsfilter
    umgesetzt, nÃ¤chster Lauf muss zeigen, ob `regulatory_overload`
    dadurch feiner aufbricht
  - Integrationsantwort fÃ¼r `integration_strain` umgesetzt:
    Sortierung, Reframing, Memory-Recall und Kontaktvertiefung werden
    diagnostisch und leicht regulativ sichtbar
  - Gerichtete Vorsicht / vorsichtige Hypothese umgesetzt:
    Vorsicht wird nicht als harte Sperre behandelt, sondern kann sich Ã¼ber
    Memory, Reframing, Kontaktvertiefung und bewusste Geduld zu
    `cautious_plan_seed`, `memory_reframe_seed`, `observe_until_clear` oder
    `deepen_contact_first` organisieren
  - Lauf 17 ausgewertet:
    zeitliche KohÃ¤renz senkt Drawdown und verbessert Profit Factor, aber
    `aged_memory_contact` dominiert fast alles
  - `active_context_activation`, `active_context_support`,
    `active_context_conflict` und `active_context_bearing` bleiben im
    Memory-Protokoll noch bei `0.0`
  - nÃ¤chster Schritt:
    zeitliche Identitaet feiner kalibrieren und den zeitlich abgeleiteten
    `active_context_trace` frÃ¼her in Memory-/Thinking-Auswertung einspeisen
  - umgesetzt:
    Zeitidentitaet bindet jetzt stÃ¤rker Ã¼ber Formfamilie, Kontext und
    grobe visuelle Signatur; feine EinzelabdrÃ¼cke bleiben als
    `temporal_source_identity` erhalten
  - umgesetzt:
    `active_context_trace` wird direkt nach der Zeitwahrnehmung gebildet
    und vor Thought-/Meta-Regulation in `world_state`, `perception_state`,
    `fused` und Runtime-Protokollpakete gelegt
  - nÃ¤chster Schritt:
    neuer Lauf; prÃ¼fen, ob `aged_memory_contact` abnimmt und
    `active_context_*` im Memory-Protokoll sichtbar wird
  - Lauf 18 ausgewertet:
    `active_context_*` ist jetzt sichtbar, aber deutlich zu hoch
    (`activation` Durchschnitt ca. `0.8905`, `support` Durchschnitt
    ca. `0.8991`, `bearing` Durchschnitt ca. `0.8493`)
  - Lauf 18 ausgewertet:
    Zeitbindung verteilt sich besser
    (`unbound_moment`, `aged_memory_contact`, erste
    `recurrent_contact`/`continued_contact`/`coherent_sequence`), aber
    Kontextvertrauen ist noch zu wenig dosiert
  - nÃ¤chster Schritt:
    aktiven Kontext nicht entfernen, sondern organisch dÃ¤mpfen und
    stÃ¤rker an Quellenbindung, Sequenzkoharenz, StrukturqualitÃ¤t und
    Gegenwartsbindung koppeln
  - umgesetzt:
    `active_context_activation` wird weich geblendet statt per `max()`
    festgehalten
  - umgesetzt:
    `reality_anchor` und `overtrust_pressure` dosieren den zeitlichen
    Kontextfaden; Support/Bearing brauchen mehr Gegenwartsbindung,
    Conflict/Fragility steigen bei ungebundenem oder schlecht geerdetem
    Kontakt
  - nÃ¤chster Schritt:
    neuer Lauf; prÃ¼fen, ob der aktive Kontext weniger sÃ¤ttigt und
    Mid/Low-Strukturen mehr natÃ¼rliche Skepsis erzeugen
  - umgesetzt:
    nervliche Ãœberlastung als Reflexionsparameter ergÃ¤nzt:
    `nervous_system_overload`, `escape_action_drive`,
    `shock_response_risk`, `nervous_overload_reflection_need`
  - Lauf 19 ausgewertet:
    starker Referenzlauf vor dieser Erweiterung
    (`pnl_netto` ca. `+39.8848`, Profit Factor ca. `1.3348`,
    Max Drawdown ca. `6.3386`), aber die neuen Nervensystem-Spalten
    fehlen noch in den Protokoll-Headern
  - nÃ¤chster Schritt:
    frischen Lauf nach Prozess-Neustart prÃ¼fen; besonders
    Stress-/Regimewechselbereiche auf Ãœberreiz, Entladungsdruck,
    Schockrisiko und reflektive Distanz auswerten
  - Lauf 20 ausgewertet:
    neue Nervensystem-Spalten sind vorhanden; Lauf bleibt positiv
    (`pnl_netto` ca. `+23.9208`, Profit Factor ca. `1.2016`), aber
    Drawdown steigt wieder auf ca. `11.6453`
  - Befund:
    `nervous_system_overload`, `escape_action_drive`,
    `shock_response_risk` und `nervous_overload_reflection_need` bleiben
    messbar, aber meist unterhalb der echten Reflexionsschwelle;
    `active_context_activation/support/bearing` bleiben im
    Memory-Protokoll weiter stark gesÃ¤ttigt
  - nÃ¤chster Schritt:
    nervliche Ãœberlastung organisch an Kontextvertrauen und
    reflektive Distanz koppeln, ohne harte Blocker einzubauen
  - umgesetzt:
    `active_context_self_certainty` und `nervous_context_overcoupling`
    ergÃ¤nzt; nervliche Last dimmt Kontext-Selbstsicherheit weich und
    erhoeht reflektive Distanz, ohne Handlung hart zu sperren
  - nÃ¤chster Schritt:
    Lauf 21 prÃ¼fen; besonders ob `nervous_context_overcoupling` in
    Stressbereichen sichtbar wird und ob `context_overcoupling_reflection`
    natÃ¼rlich auftaucht
  - Lauf 21 ausgewertet:
    `nervous_context_overcoupling` ist sichtbar
    (Durchschnitt ca. `0.1743`, Maximum ca. `0.3084`);
    `context_overcoupling_reflection` wird mit `3351` Vorkommen sogar
    hÃ¤ufigster Metaregulator-Zustand
  - Befund:
    Selbstwahrnehmung greift, aber `active_context_activation/support/bearing`
    bleiben weiter stark gesÃ¤ttigt; die Reflexion markiert die Lage,
    reguliert den aktiven Kontext aber noch nicht tief genug
  - nÃ¤chster Schritt:
    Ãœberkopplung sanft in den aktiven Kontext zurÃ¼ckfÃ¼hren, damit
    Support/Bearing bei nervlicher Faerbung weniger absolut wirken
  - umgesetzt:
    `nervous_context_overcoupling` moduliert den `active_context_trace`
    selbst; Support/Bearing/Action-Support werden weich gedimmt,
    Conflict/Fragility/Attenuation steigen leicht
  - nÃ¤chster Schritt:
    Lauf 22 prÃ¼fen; Ziel ist weniger gesÃ¤ttigter aktiver Kontext und
    weniger dominante `context_overcoupling_reflection`
  - Lauf 22 ausgewertet:
    Kontext-Rekalibrierung wirkt: `active_context_support` sinkt ca.
    `0.9007 -> 0.8856`, `active_context_bearing` ca.
    `0.8513 -> 0.8385`, `active_context_conflict` steigt ca.
    `0.1075 -> 0.1238`
  - Befund:
    DIO wird deutlich vorsichtiger (`343` Trades, mehr Observe/Withheld),
    aber PnL sinkt auf ca. `+11.8929`; die Dosis schuetzt, kostet aber
    Handlungskraft
  - nÃ¤chster Schritt:
    `context_modulation_label` im Debug sichtbar machen, bevor die
    Mechanik weiter dosiert wird
  - umgesetzt:
    `active_context_modulation_label` in
    `mcm_memory_thinking_protocol.csv` ergÃ¤nzt
  - nÃ¤chster Schritt:
    Lauf 23 prÃ¼fen; Verteilung von `unmodulated_context`,
    `nervous_tinted_context` und `overcoupled_context` mit PnL,
    Drawdown und Observe/Act-Verhalten vergleichen
  - Lauf 23 ausgewertet:
    PnL erholt sich auf ca. `+24.4854`, Trades `371`, Profit Factor
    ca. `1.2160`; `nervous_tinted_context` dominiert (`7229`),
    `overcoupled_context` bleibt sichtbar (`1504`)
  - Befund:
    Die Modulation wirkt nicht mehr nur als Bremse. DIO gewinnt
    Handlungskraft zurÃ¼ck, bleibt aber nervlich markiert. Der Drawdown
    bleibt mit ca. `15.43` hoch.
  - nÃ¤chster Schritt:
    Low-/Mid-Kontaktreifung Ã¼ber konsequenzbasiertes Feedback schaerfen:
    Low nicht hart blockieren, sondern als belastenden, unreifen oder
    reorganisationspflichtigen Kontakt im MCM-Feld erfahrbar machen
  - erweiterte Zielrichtung:
    Low-/Mid-Kontakte mit MCM-Raumzeit-Tiefe koppeln. DIO soll nicht nur
    StrukturqualitÃ¤t fÃ¼hlen, sondern auch, ob ein Kontakt durch
    Gegenwart, Nachhall, Erinnerung oder Erwartung wirkt.

- [x] MCM-Raumzeit-Tiefe technisch verdichten.
  Ziel:
  - Entfernung, Energie und Zeit als innere Wahrnehmungsschicht koppeln
  - keine harte Zeitregel, sondern Selbstverortung im MCM-Feld
  - Memory nicht nur als gespeicherte Information behandeln, sondern als
    verdichtete Erfahrung mit zeitlicher Tiefe
  - bestehende Werte wie `temporal_context_depth`,
    `memory_time_distance`, `temporal_afterimage`, `temporal_decay`,
    `perceptual_distance`, `field_attachment` und Energie-/Druckwerte
    organisch zusammenfÃ¼hren
  Erste ZielgrÃ¶ÃŸen:
  - `mcm_spacetime_depth`
  - `temporal_self_location`
  Umgesetzt:
  - `mcm_spacetime_depth`
  - `memory_experience_depth`
  - `future_projection_depth`
  - `temporal_self_location`
  - `temporal_self_location_state`
  - Export in Memory-/Field-Protokoll und `trade_stats.py`
  NÃ¤chster Schritt:
  - Debug-Lauf prÃ¼fen und danach regulatorische Kopplung entwickeln:
    flache Raumzeit-Tiefe soll nicht blockieren, sondern mehr
    Beobachtung, Reflexion oder Reorganisation nahelegen
  - Lauf 24 ausgewertet:
    PnL ca. `+23.4601`, Profit Factor ca. `1.2006`, Drawdown nur
    ca. `8.2936`; der Verlauf ist deutlich tragfÃ¤higer als Lauf 23,
    obwohl der End-PnL leicht niedriger ist
  - Befund:
    `future_possibility` dominiert, `unlocated_contact` bleibt hoch.
    DIO bildet Zukunftstiefe, aber Gegenwarts-/Memory-Verortung muss noch
    reifer werden.
  - BestÃ¤tigung:
    Lauf 24 ist ein erster positiver Hinweis, dass zeitliche Wahrnehmung
    als MCM-Welt-Tiefe wirkt: nicht als harte Regel, sondern als
    organische Entfaltung von Distanz, Reflexion und TragfÃ¤higkeit.
  - nÃ¤chster Schritt:
    regulatorische Kopplung der Raumzeit-Wahrnehmung bauen: nicht
    blockieren, sondern flache Selbstverortung in Reflexion, Beobachtung
    oder Reorganisation Ã¼bersetzen
  - umgesetzt:
    regulatorische Kopplung gebaut mit `spacetime_unlocated_pressure`,
    `spacetime_memory_bearing`, `spacetime_future_bearing`,
    `spacetime_reflection_need`, `spacetime_regulation_support` und
    `spacetime_regulation_state`
  - nÃ¤chster Schritt:
    Lauf 25 prÃ¼fen; wichtig ist, ob der Drawdown niedrig bleibt und ob
    `future_depth_watch` / `spacetime_unlocated_reflection` zu organischer
    Reflexion fÃ¼hren statt zu Ãœberregulation
  - Lauf 25 ausgewertet:
    PnL ca. `+35.7929`, Profit Factor ca. `1.3125`, Drawdown ca.
    `7.0778`; Verlauf sehr stark, Low-Schaden sinkt auf ca. `-37.93`,
    Mid wird wieder positiv
  - Einschraenkung:
    Die `spacetime_*` Regulatorwerte standen im Protokoll noch auf `0.0`.
    Damit ist Lauf 25 ein Hinweis auf die Raumzeit-Kernrichtung, aber noch
    kein Nachweis der regulatorischen Kopplung.
  - behoben:
    `spacetime_*` Werte werden jetzt im Temporal-Kern initial berechnet,
    bevor sie exportiert und spÃ¤ter in der Meta-Regulation verfeinert
    werden.
  - nÃ¤chster Schritt:
    Lauf 26 als echten Test der Raumzeit-Regulation laufen lassen
  - Lauf 26 ausgewertet:
    PnL ca. `+19.8490`, Profit Factor ca. `1.1703`, Drawdown ca.
    `8.8080`; High bleibt tragend, Mid ist deutlich positiv, Low belastet
    wieder stark.
  - Befund:
    MCM-Raumzeit-Wahrnehmung ist aktiv, aber die regulatorischen
    `spacetime_*` Werte wurden im Meta-Regulator nicht zurÃ¼ckgegeben und
    deshalb nur als `0.0` / `spacetime_open` exportiert.
  - behoben:
    RÃ¼ckgabe von `spacetime_unlocated_pressure`,
    `spacetime_memory_bearing`, `spacetime_future_bearing`,
    `spacetime_reflection_need`, `spacetime_regulation_support` und
    `spacetime_regulation_state` in `build_meta_regulation_state`
    ergÃ¤nzt.
  - nÃ¤chster Schritt:
    Neuer Lauf prÃ¼ft erstmals sichtbar, ob Raumzeit-Tiefe als
    regulatorisches Nervensignal in Reflexion, Beobachtung, Reorganisation
    oder tragender Handlung auftaucht.
  - Lauf 27 ausgewertet:
    PnL ca. `+30.9274`, Profit Factor ca. `1.2705`, Drawdown ca.
    `10.4069`; Raumzeit-Regulation ist jetzt sichtbar.
  - Befund:
    `future_depth_watch` erscheint deutlich (`~2000` Feld-/Memory-Zeilen),
    dazu kleinere Anteile `present_depth_bearing` und
    `memory_depth_bearing`. DIO beginnt damit, zeitliche Tiefe als
    innere Lage zu fÃ¼hren.
  - Grenze:
    Low bleibt negativ (`-45.0185`). Die Zeit-Tiefe erzeugt mehr
    Verortung, aber noch keine genuegende Reife im Umgang mit schwachen
    Kontakten.
  - nÃ¤chster Schritt:
    Raumzeit-Regulation mit visueller Struktur-/Kontaktwahrnehmung
    koppeln, damit DIO erkennt, ob ein Kontakt aktuell, erinnert,
    zukÃ¼nftig mÃ¶glich oder wirklich nah/tragfÃ¤hig ist.
  - umgesetzt:
    strategisches Fenster und aktives MCM-Kontaktorgan um
    `area_temporal_contact_mode`, `area_spacetime_fit`,
    `contact_temporal_mode`, `contact_temporal_bearing`,
    `contact_future_watch`, `contact_memory_depth`,
    `contact_presentness` und `contact_unlocated_pressure` erweitert.
  - Debug:
    `mcm_strategic_window_protocol.csv` und
    `mcm_active_contact_protocol.csv` schreiben die neuen Kontaktachsen.
  - nÃ¤chster Schritt:
    Neuer Lauf prÃ¼ft, ob DIO Kontakte zeitlich besser verortet:
    Gegenwart, Erinnerung, Zukunftsraum oder unverorteter Druck.
  - Lauf 28 ausgewertet:
    PnL ca. `+19.6617`, Profit Factor ca. `1.1607`, Drawdown ca.
    `10.1210`. Die Raumzeit-Kontaktachsen sind aktiv, aber sehr stark auf
    Gegenwartskontakt ausgerichtet.
  - Befund:
    `present_area_contact` ca. `10675` und `present_contact_touch` ca.
    `10257`; dagegen `future_contact_watch` ca. `166` und
    `memory_contact_recall` ca. `61`. DIO berÃ¼hrt also noch zu viel als
    aktuelles Jetzt.
  - nÃ¤chster Schritt:
    weiche Balance der Raumzeit-Kontaktmodi schaerfen, damit Zukunftsraum,
    Erinnerung und unverorteter Druck natÃ¼rlicher gegen
    Gegenwartskontakt differenziert werden.
  - umgesetzt:
    `area_current_contact` und `contact_presentness` selektiver gemacht;
    `area_future_contact`, `area_memory_contact`, `contact_future_watch`
    und `contact_memory_depth` dÃ¼rfen frÃ¼her als eigene Kontaktlage
    sprechen, wenn Gegenwart nicht klar dominiert.
  - nÃ¤chster Schritt:
    Neuer Lauf prÃ¼ft, ob `present_contact_touch` weniger dominant wird
    und ob Zukunft/Erinnerung/unverorteter Druck organischer sichtbar
    werden.
  - Lauf 29 ausgewertet:
    PnL ca. `+31.4319`, Profit Factor ca. `1.2750`, Drawdown ca.
    `8.4780`; Low-Schaden sinkt auf ca. `-41.9181`.
  - Befund:
    Balancing greift sehr stark. `future_contact_watch` dominiert mit ca.
    `8268`, `present_contact_touch` ist praktisch nicht mehr dominant.
    DIO berÃ¼hrt weniger blind die Gegenwart und beobachtet stÃ¤rker
    Zukunftsraum.
  - Grenze:
    Die Verschiebung kÃ¶nnte jetzt etwas zu stark in Zukunftsbeobachtung
    liegen. Gegenwartskontakt muss wieder organisch entstehen dÃ¼rfen,
    wenn NÃ¤he, TragfÃ¤higkeit und Reality-Check zusammenpassen.
  - nÃ¤chster Schritt:
    Ãœbergang `future_contact_watch -> present_contact_touch` weich
    modellieren, ohne in mechanische Entry-Regeln zu fallen.
  - umgesetzt:
    ReifungsbrÃ¼cke gebaut mit `area_future_to_present_readiness`,
    `contact_future_to_present_readiness`, `maturing_present_area` und
    `maturing_present_contact`.
  - nÃ¤chster Schritt:
    Neuer Lauf prÃ¼ft, ob Zukunftskontakte organisch in reife
    Gegenwartskontakte Ã¼bergehen, ohne die alte
    `present_contact_touch`-Ãœberdominanz zurÃ¼ckzuholen.
  - Lauf 30 ausgewertet:
    PnL ca. `+30.6240`, Profit Factor ca. `1.2501`, Drawdown ca.
    `13.2283`. High und Mid tragen stark, Low verschlechtert sich auf ca.
    `-50.4262`.
  - Befund:
    ReifungsbrÃ¼cke greift auf Bereichsebene:
    `maturing_present_area` ca. `3796`. Im aktiven Kontaktorgan erscheint
    aber noch kein `maturing_present_contact`; `future_contact_watch`
    bleibt dominant mit ca. `7757`.
  - nÃ¤chster Schritt:
    Kopplung von `maturing_present_area` in
    `contact_future_to_present_readiness` stÃ¤rken, damit das
    Kontaktorgan die strategische Reifung Ã¼bernehmen kann, ohne wieder in
    Gegenwarts-Ãœberdominanz zu kippen.
  - umgesetzt:
    `area_future_to_present_readiness` und `maturing_present_area` wirken
    nun direkt in `contact_future_to_present_readiness`; die finale
    Umschaltung nutzt spÃ¤ter die vollstÃ¤ndigere KontaktqualitÃ¤t
    (`contact_reality_check`, `contact_carrying_quality`,
    `outer_inner_coherence`, `contact_action_maturity`).
  - nÃ¤chster Schritt:
    Neuer Lauf prÃ¼ft, ob `maturing_present_contact` sichtbar wird.
  - Lauf 31 ausgewertet:
    PnL ca. `+29.4938`, Profit Factor ca. `1.2459`, Drawdown ca.
    `8.8692`; High und Mid tragen, Low bleibt stark negativ mit ca.
    `-50.4702`.
  - Befund:
    Reifungsleitung funktioniert. `maturing_present_contact` erscheint ca.
    `3664` mal, wÃ¤hrend `future_contact_watch` ca. `4453` bleibt. Damit
    entsteht die gewuenschte Zwischenlage zwischen Zukunftsbeobachtung und
    Gegenwartskontakt.
  - nÃ¤chster Schritt:
    Low-Kontakte qualitativ tiefer auswerten: Welche Low-Kontakte werden
    trotz Reifung zu schmerzhaften Handlungen? Daraus weiche
    KontaktqualitÃ¤ts-Reorganisation ableiten.
  - umgesetzt:
    Positions-Erleben als neurochemische MCM-Feldschicht ergÃ¤nzt.
    `position_inconsistency_stress`, `position_mcm_field_strain`,
    `position_self_trust_gap`, `position_cortisol_load`,
    `position_noradrenaline_arousal`, `position_protective_distance`,
    `position_held_risk_discomfort`, `position_process_quality` und
    `position_experience_label` werden nun in Positionsdebug,
    Outcome-Kontext und In-Trade-Memory-Zusammenfassung mitgefÃ¼hrt.
  - nÃ¤chster Schritt:
    Neuer Lauf prÃ¼ft, ob Low-/Mid-Verluste mit hoher
    `position_inconsistency_stress`, hoher `position_cortisol_load` oder
    niedriger `position_process_quality` zusammenfallen. Ziel bleibt
    Selbstschutz und Reifung, keine harte Sperre.
  - Lauf 32 ausgewertet:
    PnL ca. `+30.0961`, Profit Factor ca. `1.2582`, Drawdown ca.
    `11.4720`; High trÃ¤gt sehr stark, Mid fÃ¤llt zurÃ¼ck, Low bleibt
    negativ, ist aber weniger schmerzhaft als Lauf 31.
  - Befund:
    Die Positions-Erlebensschicht ist lesbar. Low-Verluste zeigen im
    Mittel hohe `position_noradrenaline_arousal` ca. `0.5915`, hohen
    `position_held_risk_discomfort` ca. `0.7321`, niedrige
    `position_process_quality` ca. `0.3696` und meist
    `protective_stress_contact`.
  - nÃ¤chster Schritt:
    `position_experience_label` und Positionsstress in das
    konsequenzbasierte Feedback zurÃ¼ckfÃ¼hren. Ziel:
    Formfamilien sollen belastende offene Konsequenzen als Vorsicht,
    Schmerzspur, Reorganisation oder reiferen Umgang lernen, ohne dass
    daraus eine harte Low-/Mid-Sperre entsteht.
  - umgesetzt:
    Positions-Erleben wirkt nun weich in die Formsymbol-Entwicklung:
    `position_consequence_burden`, `position_constructive_bearing` und
    `position_feedback_label` werden beim Outcome gebildet und in
    `outcome_records.jsonl` sichtbar.
  - nÃ¤chster Schritt:
    Neuer Lauf prÃ¼ft, ob belastete Low-/Mid-Kontakte nicht blockiert,
    sondern hÃ¤ufiger als `protective_reorganization_contact`,
    `careful_contact` oder gereifter Beobachtungskontakt gelernt werden.

- [ ] Markdown-Dateien weiter nach `MD_ANWEISUNG.md` pflegen.
  Ziel:
  - keine doppelten Laufanalysen
  - `FIX_LISTE.md` aktiv und kurz halten
  - `AKTUELLER_STAND.md` kompakt halten
  - `WICHTIG_MECHANIKEN.md` technisch halten
  Status:
  - Umsetzungsplan strukturell bereinigt
  - `ENDE` ans echte Dateiende gebracht
  - Affective-Pattern-Block sauberer eingeordnet

- [ ] Variablen-Audit auf doppelte Funktionsdeutung fortsetzen.
  Status:
  - `MCM_VARIABLEN_MECHANIK.md` geprÃ¼ft: `331` VariablenuÌˆberschriften,
    keine exakt doppelten Namen.
  - fehlende `Funktion:`-Zeilen fÃ¼r `sensory_reality_label`,
    `trust_transfer_mode` und `target_expectation_context` ergÃ¤nzt.
  - Konvention gegen doppelte Funktionsdeutung ergÃ¤nzt.
  PrÃ¼fgruppen:
  - Last/Druck/Stress
  - Distanz/Reflexion
  - TragfÃ¤higkeit/QualitÃ¤t
  - Kontaktlernen
  - Reorganisation/Reframing
  NÃ¤chster Schritt:
  - Variablen-Hierarchie bauen:
    Basisreiz -> Kontakt -> Position -> Outcome-Sample -> Memory ->
    Neurochemie/Diagnose.
  - Danach entscheiden, ob einzelne Achsen Alias bleiben, klarer getrennt
    oder zusammengelegt werden.
  - Ãœberlappungs-Audit ergÃ¤nzt:
    Ãœberlappung ist organisch erlaubt, wenn andere Rezeptoren, Ebenen oder
    Zeitlagen beteiligt sind.
  - PrÃ¼fpflichtige Rezeptorkaskaden:
    Last-Kaskade, Reorganisation-Kaskade, Distanz-Kaskade,
    TragfÃ¤higkeits-Kaskade.
  - nÃ¤chster Schritt:
    Rezeptor-Matrix anlegen:
    `Signal -> Rezeptorfamilie -> Zielregler -> Wirkung -> Speicher?`.
    Damit wird sichtbar, ob Signale denselben Zielregler doppelt belasten.
  - umgesetzt:
    `MCM_REZEPTOR_MATRIX.md` angelegt und in `MD_ANWEISUNG.md` als eigener
    Dokumentationsort fÃ¼r Wirkpfade/Rezeptoren eingetragen.
  - nÃ¤chster Schritt:
    Matrix aus dem Code weiter konkretisieren:
    `Signal -> Rezeptorfamilie -> Zielregler -> Wirkung -> Speicherstatus`.
    Besonders prÃ¼fen:
    Last-Kaskade, Distanz-Kaskade, Reorganisations-Kaskade und
    TragfÃ¤higkeits-Kaskade.
  - Lauf 33 Befund:
    Das neue Positionsfeedback ist sichtbar. TP wird Ã¼berwiegend als
    `carried_position_contact` gelesen, SL Ã¼berwiegend als
    `protective_stress_contact`. Gleichzeitig steigt
    `protective_reorganization_contact` stark an.
  - nÃ¤chster Schritt:
    Rezeptor-Matrix gegen Code prÃ¼fen:
    Wir mÃ¼ssen sicherstellen, dass `position_consequence_burden` als
    verdichtete Outcome-Last wirkt und nicht zusammen mit seinen Vorachsen
    dieselbe Schmerz-/Carefulness-Spur mehrfach verstÃ¤rkt.
  - umgesetzt:
    Weiche Rezeptor-SÃ¤ttigung ergÃ¤nzt:
    `position_consequence_residual_for_care` und
    `position_consequence_residual_for_memory` verhindern, dass dieselbe
    Positionslast ungefiltert mehrfach auf Schmerz, Vorsicht und Memory
    wirkt.
  - nÃ¤chster Schritt:
    Neuer Lauf prÃ¼ft die Verteilung von `protective_reorganization_contact`,
    `careful_contact`, `burdened_contact` und `constructive_contact`.
  - Lauf 34 Befund:
    Rezeptor-SÃ¤ttigung wirkt: `contact_carefulness_sample` sinkt deutlich,
    wÃ¤hrend `contact_pain_sample` stabil bleibt. Low-Schaden wird kleiner,
    aber Mid verliert TragfÃ¤higkeit.
  - nÃ¤chster Schritt:
    Mid-Kontakt-Reifung prÃ¼fen/umsetzen:
    Nicht SÃ¤ttigung zurÃ¼cknehmen, sondern besser unterscheiden, ob ein
    mittlerer Kontakt Ã¼ber `position_constructive_bearing`,
    `contact_temporal_bearing`, `area_bearing_quality` und
    `contact_reality_check` wirklich reift oder nur offen/neutral bleibt.
  - umgesetzt:
    `transitional_contact_band` und `transitional_contact_maturation`
    ergÃ¤nzt. Die Achsen wirken nur im Outcome-Lernen und stÃ¤rken
    Kontaktreife/Utility leicht, wenn ein uneindeutiger Kontakt zeitlich,
    raeumlich und prozessual tragfÃ¤hig wird.
  - nÃ¤chster Schritt:
    Neuer Lauf prÃ¼ft Mid-PnL, `transitional_contact_maturation`,
    `contact_maturity_sample`, `contact_utility_sample` und die
    Kontaktlernzustands-Verteilung.
  - umgesetzt:
    Unterbewusste Nachhall-Tiefenwahrnehmung ergÃ¤nzt:
    `subconscious_afterimage_depth`, `subconscious_afterimage_pressure`,
    `subconscious_afterimage_bearing`, `subconscious_afterimage_clarity`,
    `subconscious_afterimage_release` und
    `subconscious_afterimage_reflection_pull`.
    Die Achsen bilden keinen harten Schalter, sondern eine weiche
    Kompression alter Feldwirkung. Unklarer tiefer Nachhall zieht DIO eher
    in Beobachtung/Reflexion und reduziert Handlung nur leicht.
  - nÃ¤chster Schritt:
    Neuer Lauf prÃ¼ft, ob Nachhall als eigener Tiefenzustand sichtbar wird:
    Druck hoch, Klarheit/Release niedrig -> mehr reflektiver Abstand;
    TragfÃ¤higkeit/Klarheit hoch -> Nachhall kann als Erfahrung getragen
    werden.
  - Lauf 34 Befund:
    Der Lauf enthÃ¤lt die neuen `subconscious_afterimage_*`-Spalten noch
    nicht und kann die neue Tiefen-Nachhall-Schicht daher nicht direkt
    prÃ¼fen. Ergebnis: ca. `+18.2779` Netto-PnL, `342` Trades,
    `131/211` TP/SL. High bleibt stark, Low ist weniger schadhaft, Mid
    bleibt der Hauptverlustbereich.
  - nÃ¤chster Schritt:
    Neuen Lauf mit aktueller Mechanik starten. Danach speziell prÃ¼fen:
    Fallen Mid-Verluste mit hohem `subconscious_afterimage_pressure`,
    niedriger `subconscious_afterimage_clarity` und niedriger
    `subconscious_afterimage_release` zusammen?
  - Lauf 35 Befund:
    Neue Nachhall-Spalten sind aktiv. Ergebnis ca. `+18.2048` Netto-PnL,
    `345` Trades, `135/210` TP/SL, Drawdown ca. `8.8596`.
    Nachhall ist stabil messbar, wirkt im Feld bei `act_watch` etwas
    stÃ¤rker reflektiv, unterscheidet aber in abgeschlossenen Outcomes TP
    und SL noch kaum. Strategische Fensterwahrnehmung ist aktiv
    (`bearing_area_hypothesis` dominiert), aber alle Entries bleiben
    `impulse_contact` mit `strategic_entry_weight = 0.0`.
  - nÃ¤chster Schritt:
    Weiche motorische Alternative fÃ¼r strategische Bereichswahrnehmung
    bauen: `area_order_intention` und `area_bearing_quality` dÃ¼rfen eine
    `area_contact_intention` nahelegen, ohne Impuls-Trades hart zu ersetzen
    oder Bereichshandel zu erzwingen.
  - umgesetzt:
    `area_motor_intention` und `area_motor_distance_fit` ergÃ¤nzt.
    `entry_mode` kann nun `area_contact_intention` annehmen.
    `strategic_entry_weight` wird weicher aus `strategic_entry_fit` und
    `area_motor_intention` gebildet. Das bleibt eine FÃ¤higkeit, keine
    Pflicht.
  - nÃ¤chster Schritt:
    Neuer Lauf prÃ¼ft:
    Wie oft entstehen `impulse_contact`, `area_contact_intention` und
    `area_contact_entry`? Tragen Bereichsentries besser im Mid-Bereich oder
    erzeugen sie zusÃ¤tzliche Unsicherheit?
  - Runtimefix:
    `area_spacetime_fit is not defined` in `derive_trade_plan_from_brain`
    behoben. Der Wert wird jetzt vor `area_motor_intention` aus dem
    gewÃ¤hlten Bereich gelesen.
  - PrÃ¼fung:
    `py_compile` und eine direkte Funktionssimulation laufen sauber.
    Simulation erzeugte `area_contact_intention` mit positivem
    `strategic_entry_weight`.
  - umgesetzt:
    Feste RR-Konfiguration bereinigt:
    `RR`, `MAX_RR` und `MCM_EXCITED_RR_FACTOR` aus `config.py` entfernt.
    Alte `Config.RR`-Fallbacks wurden durch dynamische RR-Ableitungen
    ersetzt. `MIN_RR` bleibt als technische Sicherheitsuntergrenze,
    `RR_EXECUTION_MIN` bleibt als Live-Ausfuehrungsschutz.
  - nÃ¤chster Schritt:
    Neuer Lauf prÃ¼ft `rr_value`-Streuung nach `entry_mode`:
    `impulse_contact` gegen `area_contact_intention`, besonders im
    Mid-Bereich.
  - Lauf 36 Befund:
    RR-Bereinigung wirkt stark: Netto-PnL ca. `+37.2357`, `369` Trades,
    `155/214` TP/SL, Drawdown ca. `5.7776`. RR streut organisch
    (`p10` ca. `1.895`, Median ca. `4.439`, `p90` ca. `5.134`).
    Alle Entries bleiben jedoch `impulse_contact`; `strategic_entry_weight`
    und `area_motor_intention` bleiben im echten Lauf `0.0`.
  - nÃ¤chster Schritt:
    Schnittstelle zwischen strategischem Fenster und Trade-Plan prÃ¼fen.
    Der Trade-Plan braucht den vollstÃ¤ndigen `strategic_window_state`
    inklusive Kandidaten/Fokus, damit `area_contact_intention` real aus dem
    Sehen in die Motorik gelangt.
  - umgesetzt:
    `derive_trade_plan_from_brain(...)` nimmt `strategic_window_state` und
    `form_symbol_state` jetzt direkt entgegen. Runtime Ã¼bergibt den frisch
    berechneten Zustand an virtuellen Beobachtungsplan und echten Trade-Plan.
  - PrÃ¼fung:
    `py_compile` sauber. Direkte Funktionssimulation ohne Bot-State erzeugt
    `area_contact_intention` mit positivem `strategic_entry_weight`.
  - nÃ¤chster Schritt:
    Neuer Lauf prÃ¼ft, ob die Bereichsmotorik jetzt im echten Debug
    tatsÃ¤chlich erscheint.
  - Lauf 37 Befund:
    Direkte Ãœbergabe reicht noch nicht. Ergebnis ca. `+22.3768` Netto-PnL,
    `356` Trades, `144/212` TP/SL, Drawdown ca. `10.1675`.
    Alle Entries bleiben `impulse_contact`; `area_contact_intention`,
    `strategic_entry_weight` und `area_motor_intention` entstehen im echten
    Lauf weiterhin nicht.
  - nÃ¤chster Schritt:
    Entry-Wahlwahrnehmung bauen:
    DIO soll die zwei MÃ¶glichkeiten innerlich als Alternative erkennen:
    Impuls-Entry gegen Bereichs-Entry. Dazu Diagnose-/Regelkreiswerte wie
    `impulse_entry_intention`, `area_entry_intention`,
    `entry_choice_conflict`, `entry_choice_bearing` und
    `entry_choice_state` ergÃ¤nzen.
  - umgesetzt:
    Entry-Wahlwahrnehmung im Trade-Plan, Runtime-Result, kompakten
    Tradeplan-Export und `MCM_VARIABLEN_MECHANIK.md` ergÃ¤nzt.
    Die Schicht ist weich: sie beschreibt eine innere Wahlspannung zwischen
    Impuls und Bereich, ohne eine mechanische Pflichtentscheidung zu setzen.
  - nÃ¤chster Schritt:
    Neuer Lauf prÃ¼ft die Verteilung von `entry_choice_state`,
    `impulse_entry_intention`, `area_entry_intention` und ob daraus erstmals
    reale `area_contact_intention` entsteht.
  - Lauf 38 Befund:
    Ergebnis ca. `+43.8965` Netto-PnL, `369` Trades, `160/209` TP/SL.
    Die Bereichswahrnehmung ist im strategischen Fenster sichtbar, aber der
    echte Trade-Plan bleibt `impulse_contact` / `impulse_only`.
    Posthoc mit denselben strategischen Fensterdaten entstehen dagegen viele
    `area_contact_intention`-FÃ¤lle. Engpass ist deshalb die Kopplung
    zwischen bewusster Bereichswahrnehmung und Motorik.
  - umgesetzt:
    weiche Entry-Synchronisation im Runtime-Ergebnis ergÃ¤nzt:
    Wenn ein Plan noch `impulse_only` ist, aber ein strategisches
    Bereichsfenster vorhanden ist, wird der Trade-Plan mit dieser
    Wahrnehmung erneut integriert. Neuer Diagnosewert: `entry_choice_sync`.
  - nÃ¤chster Schritt:
    Neuer Lauf prÃ¼ft, ob `entry_choice_sync=strategic_context_integrated`
    und `area_contact_intention` im echten Debug erscheinen.
  - Lauf 39 Befund:
    Ergebnis ca. `+20.2809` Netto-PnL, `331` Trades, `132/199` TP/SL.
    DIO beobachtet/enthÃ¤lt sich mehr (`withheld` und `observed` hÃ¶her),
    aber `entry_choice_sync` bleibt im Trade-Plan `-` und alle Entries
    bleiben `impulse_contact`.
  - umgesetzt:
    Entry-Synchronisation vom nachtrÃ¤glichen Runtime-Ergebnis in den
    eigentlichen `prices`-/Trade-Plan-Aufbau vorgezogen. Dadurch wird die
    Bereichswahrnehmung vor der Ergebnisbildung integriert.
  - nÃ¤chster Schritt:
    Neuer Lauf prÃ¼ft, ob `entry_choice_sync` jetzt Werte wie
    `strategic_context_integrated`, `impulse_context_kept` oder
    `native_choice_state` zeigt und ob Bereichs-Entries entstehen.
  - Lauf 40/41 Befund:
    Lauf 40 ca. `+21.2217` Netto-PnL, `337` Trades, `134/203` TP/SL.
    Lauf 41 ca. `+13.9366` Netto-PnL, `327` Trades, `130/197` TP/SL.
    Beide LÃ¤ufe zeigen weiter nur `impulse_contact`, `impulse_only` und
    `entry_choice_sync=-`.
  - Diagnose:
    Da der aktuelle Code `entry_choice_sync` direkt im Runtime-Plan setzt,
    deuten diese LÃ¤ufe darauf hin, dass sie noch mit einem alten geladenen
    Python-Prozess entstanden sind.
  - nÃ¤chster Schritt:
    Bot/Backtest-Prozess neu starten und Lauf 42 erzeugen. Erst dieser Lauf
    prÃ¼ft die aktuelle Entry-Synchronisation sauber.
  - Lauf 42 Befund:
    Ergebnis ca. `+35.7606` Netto-PnL, `351` Trades, `148/203` TP/SL.
    Die strategische Bereichswahrnehmung bleibt aktiv, aber im
    Attempt-Kontext bleiben `entry_choice_sync=-`,
    `entry_choice_state=impulse_only` und `area_motor_intention=0.0`.
  - Ursache:
    `bot_gate_funktions.py` hat beim finalen Entry-Return die neuen
    Entry-Wahlfelder nicht weitergereicht. Die Signale wurden damit an der
    Gate-Schnittstelle abgeschnitten.
  - umgesetzt:
    `entry_mode`, `strategic_entry_weight`, `area_motor_intention`,
    `impulse_entry_intention`, `area_entry_intention`,
    `entry_choice_conflict`, `entry_choice_bearing`,
    `entry_choice_state`, `entry_choice_sync` und strategische Bereichspreise
    werden jetzt durch `bot_gate_funktions.py` weitergereicht und in
    `entry_debug.csv` sichtbar gemacht.
  - nÃ¤chster Schritt:
    Lauf 43 prÃ¼ft die echte Durchleitung bis `attempt_records`.
  - Lauf 43 Befund:
    Die Durchleitung ist bestÃ¤tigt. `attempt_records.jsonl` enthÃ¤lt jetzt
    `entry_mode`, `entry_choice_state` und `entry_choice_sync`.
    Verteilung im Attempt-Kontext:
    `impulse_contact=1041`, `area_contact_intention=716`,
    `area_contact_entry=60`.
    In abgeschlossenen Outcomes trÃ¤gt `area_contact_intention` positiv
    (ca. `+38.0107`), wÃ¤hrend `area_contact_entry` noch leicht negativ ist
    (ca. `-0.9201`).
  - nÃ¤chster Schritt:
    Bereichskontakt nicht hÃ¤rter machen, sondern die Reife der direkten
    `area_contact_entry`-FÃ¤lle neurochemisch lesen: Warum wird aus
    tragender Bereichswahrnehmung manchmal zu frÃ¼her oder zu naher Kontakt?
  - umgesetzt:
    Weiche direkte Kontaktreife ergÃ¤nzt:
    `area_direct_readiness` beschreibt, ob ein Bereich nicht nur gesehen,
    sondern auch direkt motorisch berÃ¼hrbar wirkt.
    `area_motor_restraint` beschreibt die natÃ¼rliche ZurÃ¼ckhaltung bei
    Konflikt, unreifem Kontakt, Nachhall oder fehlender Reife.
    Konflikt darf weiter sichtbar bleiben, zieht aber weniger stark in einen
    direkten `area_contact_entry`.
  - PrÃ¼fung:
    `py_compile` fÃ¼r `MCM_Brain_Modell.py`, `bot.py`,
    `bot_gate_funktions.py` und `trade_stats.py` sauber.
  - nÃ¤chster Lauf:
    Lauf 44 prÃ¼ft, ob direkte Bereichsentries seltener, reifer oder
    tragfÃ¤higer werden und ob `area_direct_readiness` /
    `area_motor_restraint` im Debug sauber erscheinen.

- [x] Emergente Strukturdeutung im Outcome sichtbar machen.
  Ziel:
  - hohe RR-Trades nicht nur als Zahl lesen
  - unterscheiden zwischen weitem Zielraum und tragender Strukturdeutung
  - keine harte Regel, nur Diagnose-/Auswertungsschicht
  Umgesetzt:
  - `outcome_records.jsonl` enthÃ¤lt kÃ¼nftig:
    `rr_value`, `structural_run_room`,
    `emergent_structure_reading`,
    `emergent_structure_confirmation`,
    `emergent_structure_state`,
    `target_expectation_value`
  - `MCM_VARIABLEN_MECHANIK.md` dokumentiert die neuen Felder.
  PrÃ¼fung:
  - `py_compile` fÃ¼r `trade_stats.py` sauber.
  NÃ¤chster Lauf:
  - Lauf 44 nach hohen RR-Trades auswerten:
    `confirmed_structural_interpretation`,
    `open_structural_hypothesis`,
    `wide_target_without_structure`.

- [x] Einfache DIO-GUI proportional kompakter setzen.
  Ziel:
  - gleiche Inhalte behalten
  - keine weiteren Datenfelder entfernen
  - Fenster und DiagrammflÃ¤chen um 20 % kleiner anordnen
  Umgesetzt:
  - Hauptfenster, Markt, Stats, Candle, Backtest und Equity proportional
    verkleinert.
  - MindestgrÃ¶ÃŸe ebenfalls proportional auf `960x560` gesetzt.
  - Matplotlib-Figuren passend mit skaliert.
  PrÃ¼fung:
  - `py_compile` fÃ¼r `_gui.py` sauber.

- [x] Lauf 44 und emergente Strukturdeutung prÃ¼fen.
  Ergebnis:
  - Lauf 44: `+30.1462` Netto-PnL, `327` Trades, Profit Factor ca. `1.31`.
  - High-Strukturen tragen deutlich, Low-Strukturen bleiben belastend.
  - Robust gelesen:
    `confirmed_structural_interpretation` = `38` FÃ¤lle, alle TP, ca.
    `+38.99` PnL.
  - `open_structural_hypothesis` = `144` FÃ¤lle, Ã¼berwiegend SL, ca.
    `-33.91` PnL. Diese Schicht ist noch unreif und darf nicht mit
    bestÃ¤tigter Struktur verwechselt werden.
  Umsetzung:
  - `trade_stats.py` schreibt die emergente Strukturdeutung kÃ¼nftig direkt in
    `outcome_records.jsonl`.
  - `trade_stats.json` erhÃ¤lt `kpi_summary.emergent_structure`.
  PrÃ¼fung:
  - `py_compile` fÃ¼r `trade_stats.py` sauber.

- [x] Lauf 45 und Wiederholung der Strukturtrennung prÃ¼fen.
  Ergebnis:
  - Lauf 45: `+27.8990` Netto-PnL, `339` Trades, Profit Factor ca. `1.26`.
  - `confirmed_structural_interpretation`: `49` FÃ¤lle, `49` TP, `0` SL,
    ca. `+54.16` PnL.
  - `open_structural_hypothesis`: `154` FÃ¤lle, `20` TP, `134` SL,
    ca. `-39.09` PnL.
  - Damit bestÃ¤tigt sich: hohe RR-Struktur ist nur tragend, wenn sie auch
    bestÃ¤tigt und prozessqualitativ getragen ist.
  Umsetzung:
  - Cancel-Outcomes bekommen kÃ¼nftig ebenfalls direkte
    `emergent_structure_*`-Felder.
  PrÃ¼fung:
  - `py_compile` fÃ¼r `trade_stats.py` sauber.
  NÃ¤chster Mechanikpunkt:
  - Offene Strukturhypothesen nicht blockieren, sondern als unreif erkennen
    und eher in Beobachtung, Replay oder Reifung halten.

- [x] Emergente GedÃ¤chtnisspur als innere Denkschicht diagnostisch vorbereiten.
  Ziel:
  - offene Strukturhypothesen nicht lÃ¶schen und nicht hart sperren
  - Gedankenkeime aus der akuten Motorik lÃ¶sen und als innere Spur speichern
  - eigene DIO-Syntax fÃ¼r Gedanken zulassen
  - Wiederkehr, Variation, Verdichtung und Reifung messbar machen
  - RealitÃ¤tsbindung sichern, damit keine freie Halluzinationsschicht entsteht
  MÃ¶gliche Felder:
  - `emergent_memory_trace`
  - `thought_seed_id`
  - `thought_seed_label`
  - `thought_trace_strength`
  - `thought_recall_potential`
  - `thought_maturity`
  - `reality_binding_score`
  - `hallucination_drift_risk`
  - `form_symbol_anchor`
  - `mcm_field_anchor`
  - `experience_memory_anchor`
  - `outcome_anchor`
  Wichtig:
  - keine Handlungssperre
  - keine freie Fantasieschicht
  - Nicht-Handlung als Erfahrung behandeln
  - MCM als SelbstspÃ¼r- und Reflexionsanker verwenden
  Metaregulatorische Bindung:
  - Gedankenkeime nicht direkt motorisch entladen
  - Gedankenkeime nicht hart blockieren
  - `seed_focus`, `seed_replay`, `seed_mature`, `seed_store`,
    `seed_release`, `seed_action_ready`, `seed_drift_watch`,
    `seed_overthinking_watch` als mÃ¶gliche ZustÃ¤nde prÃ¼fen
  - RealitÃ¤tsbindung Ã¼ber Form, MCM-Feld, Erfahrung und spÃ¤tere Konsequenz
    sichern
  - GrÃ¼belkaskaden und Ãœberregulation diagnostisch sichtbar machen
  Umsetzung:
  - `mcm_thought_seed_protocol.csv` ergÃ¤nzt
  - `seed_metaregulator_state` diagnostisch eingefÃ¼hrt
  - keine MotorikÃ¤nderung, keine Handlungssperre

- [ ] Emergent Memory Trace spÃ¤ter an Memory-Reifung koppeln.
  Ziel:
  - erst nach Auswertung mehrerer LÃ¤ufe entscheiden
  - keine direkte Trade-Regel
  - Thought-Seeds nur dann in Memory-Reifung Ã¼bernehmen, wenn
    RealitÃ¤tsbindung, Wiederkehr und Konsequenz tragend genug sind
  - Drift- und ÃœberdenkzustÃ¤nde nicht als Strategie behandeln

- [x] Thought-Seed-Diagnose mit Outcome-BestÃ¤tigung synchronisieren.
  Befund aus Lauf 46:
  - Outcome erkennt `confirmed_structural_interpretation`
  - Thought-Seed-Diagnose bleibt noch bei `open_structural_hypothesis`
  - `reality_binding_score` ist vorsichtiger als die spÃ¤tere Konsequenz
  Umsetzung:
  - `thought_confirmation_score` oder bessere `reality_binding_score`
    ergÃ¤nzt
  - keine Motorikregel
  - nur innere Sprache schÃ¤rfen: offene Idee, reifende Idee,
    bestÃ¤tigte Idee, driftende Idee

- [x] Thought-Seed-Synchronisierung in Lauf 48 geprÃ¼ft.
  Ziel:
  - prÃ¼fen, ob `confirmed_structural_interpretation` im
    `mcm_thought_seed_protocol.csv` sichtbar wird
  - prÃ¼fen, ob `seed_action_ready` nur bei ausreichend geerdeten Gedanken
    auftaucht
  - keine Memory-Kopplung vor dieser Auswertung
  Lauf 47:
  - noch keine `confirmed_structural_interpretation` im Seed-Protokoll
  - noch kein `seed_action_ready`
  - `seed_mature` steigt aber von `185` auf `245`
  NachrÃ¼stung:
  - Thought-Seed wird ab Lauf 48 in Entry-/Outcome-Kontext Ã¼bernommen
  - direkte Kette `Gedankenkeim -> Trade -> Konsequenz` prÃ¼fen
  Befund Lauf 48:
  - `399 / 399` Outcome-EintrÃ¤ge haben eine `thought_seed_id`
  - direkte Kette ist damit technisch sichtbar
  - Seed-Protokoll bleibt innerlich vorsichtig und benennt noch keine
    bestÃ¤tigte Struktur als eigenes Seed-Ereignis

- [x] Thought-Seed-Innensprache organisch nachgeschÃ¤rft.
  Ziel:
  - bestÃ¤tigte Konsequenzspuren besser mit reifenden Gedankenkeimen verbinden
  - offene Strukturhypothesen, bestÃ¤tigte Strukturdeutung und Replay/Store
    sauberer unterscheiden
  - keine harte Handlungssperre, keine Motorikregel
  - Fokus: bessere Selbstwahrnehmung der eigenen Gedankenkeime
  Umsetzung:
  - `consequence_echo` ergÃ¤nzt
  - `reorganization_echo` ergÃ¤nzt
  - `thought_consequence_alignment` ergÃ¤nzt
  - Felder in `mcm_thought_seed_protocol.csv` und `outcome_records.jsonl`
    Ã¼bernommen
  - `py_compile` und Smoke-Test sauber

- [ ] NÃ¤chsten Lauf mit Thought-Seed-Konsequenz-Echo prÃ¼fen.
  Ziel:
  - prÃ¼fen, ob `seed_action_ready` im echten Lauf auftaucht
  - prÃ¼fen, ob `confirmed_structural_interpretation` im
    `mcm_thought_seed_protocol.csv` sichtbar wird
  - `thought_consequence_alignment` gegen TP/SL und offene Hypothesen lesen
  - keine MotorikÃ¤nderung vor dieser Auswertung
  Lauf 49:
  - `seed_action_ready` taucht noch nicht auf
  - `confirmed_structural_interpretation` bleibt im Seed-Protokoll aus
  - Outcome bestÃ¤tigt aber weiter `46/46` bestÃ¤tigte Strukturdeutungen
  - `thought_consequence_alignment` trennt bestÃ¤tigte und offene Strukturen
    noch zu schwach
  NachrÃ¼stung:
  - `thought_consequence_balance` ergÃ¤nzt
  - `thought_reality_lag` ergÃ¤nzt

- [ ] Thought-Seed-Balance im nÃ¤chsten Lauf prÃ¼fen.
  Ziel:
  - prÃ¼fen, ob bestÃ¤tigte Strukturen positivere `thought_consequence_balance`
    zeigen als offene Hypothesen
  - prÃ¼fen, ob bestÃ¤tigte Strukturen kleineres `thought_reality_lag` zeigen
  - keine Schwellenlockerung, solange die Trennung nicht sichtbar ist
  Lauf 50:
  - Trennung ist noch zu schwach
  - bestÃ¤tigte Strukturen und offene Hypothesen liegen bei Balance/Lag zu nah
    beieinander
  NachrÃ¼stung:
  - `thought_structural_grounding` ergÃ¤nzt
  - `thought_open_hypothesis_pressure` ergÃ¤nzt

- [ ] Thought-Seed-Erdung im nÃ¤chsten Lauf prÃ¼fen.
  Ziel:
  - prÃ¼fen, ob `thought_structural_grounding` bestÃ¤tigte Strukturen klarer
    von offenen Hypothesen trennt
  - prÃ¼fen, ob `thought_open_hypothesis_pressure` bei schlechten offenen
    Hypothesen erhÃ¶ht ist
  - keine MotorikÃ¤nderung vor dieser Auswertung
  Lauf 51:
  - PnL erholt sich auf ca. `+40.03`
  - Drawdown sinkt wieder auf ca. `5.11 %`
  - `thought_structural_grounding` trennt bestÃ¤tigte und offene Struktur noch
    nicht ausreichend
  - `thought_open_hypothesis_pressure` ist bei bestÃ¤tigter Struktur und
    offener Hypothese Ã¤hnlich hoch

- [x] Outcome-Lernspur fÃ¼r offene Hypothesen gebaut.
  Ziel:
  - offene Hypothesen nach spÃ¤terer Konsequenz als tragend, belastend oder
    reorganisierend auswertbar machen
  - keine Handlungssperre
  - keine Motorikregel
  - Grundlage fÃ¼r spÃ¤tere innere Reifung der Gedankensprache schaffen
  Umsetzung:
  - `open_hypothesis_learning_state`
  - `open_hypothesis_consequence_score`
  - `open_hypothesis_burden_score`
  - `open_hypothesis_reorganization_score`
  - `kpi_summary.open_hypothesis_learning`

- [ ] Outcome-Lernspur fÃ¼r offene Hypothesen im nÃ¤chsten Lauf prÃ¼fen.
  Ziel:
  - Verteilung `carried / burdened / reorganizing` prÃ¼fen
  - PnL, Erdung, Lag und Hypothesendruck je Gruppe vergleichen
  - erst danach entscheiden, ob diese Lernspur in die Thought-Seed-Reifung
    zurÃ¼ckgefÃ¼hrt wird
  Lauf 52:
  - `open_hypothesis_carried`: `24`, `+21.96` PnL, `24/24` TP
  - `open_hypothesis_burdened`: `150`, `-65.47` PnL, `150/150` SL
  - `open_hypothesis_reorganizing`: `0`
  Befund:
  - Lernspur trennt getragen und belastet sehr sauber
  - mittlere Reorganisationslage fehlt noch

- [x] Reorganisationsspur fÃ¼r offene Hypothesen geschÃ¤rft.
  Ziel:
  - nicht nur gut/schlecht unterscheiden
  - Grauzonen als Reframing-/Reorganisationslage sichtbar machen
  - keine Handlungssperre
  - Grundlage fÃ¼r gereiftere spÃ¤tere WiederprÃ¼fung offener Gedanken
  Umsetzung:
  - `open_hypothesis_reorganizing` kann jetzt entstehen, wenn
    Reorganisationsdruck hoch ist und Belastung nicht klar dominiert
  - bleibt rein rÃ¼ckblickende Lernspur

- [ ] Reorganisationsspur im nÃ¤chsten Lauf prÃ¼fen.
  Ziel:
  - prÃ¼fen, ob `open_hypothesis_reorganizing` entsteht
  - prÃ¼fen, ob diese Gruppe zwischen `carried` und `burdened` liegt
  - keine RÃ¼ckkopplung in Motorik vor dieser Auswertung
  Lauf 53:
  - `open_hypothesis_carried`: `23`, ca. `+25.85`, `23/23` TP
  - `open_hypothesis_burdened`: `24`, ca. `-10.79`, `24/24` SL
  - `open_hypothesis_reorganizing`: `127`, ca. `-54.35`, `127/127` SL
  Befund:
  - dritte Lernlage entsteht
  - sie ist aber noch Verlust-Reorganisation, keine entlastete Grauzone

- [ ] Reorganisationslage spÃ¤ter als Replay-/Abstandsbedarf koppeln.
  Ziel:
  - `open_hypothesis_reorganizing` nicht als Handlungsmut behandeln
  - als Bedarf fÃ¼r Replay, Abstand und Neudeutung sichtbar machen
  - keine harte Handlungssperre
  - zuerst diagnostisch/rÃ¼ckwirkend, dann mÃ¶gliche Thought-Seed-Reifung prÃ¼fen
  Umsetzung:
  - `open_hypothesis_replay_need`
  - `open_hypothesis_distance_need`
  - `open_hypothesis_reinterpretation_need`
  - KPI-Mittelwerte `avg_replay_need`, `avg_distance_need`,
    `avg_reinterpretation_need`

- [ ] ReorganisationsbedÃ¼rfnisse im nÃ¤chsten Lauf prÃ¼fen.
  Ziel:
  - prÃ¼fen, ob `reorganizing` ein eigenes Replay-/Distanz-/Neudeutungsprofil
    zeigt
  - prÃ¼fen, ob diese Profile von `carried` und `burdened` unterscheidbar sind
  - keine RÃ¼ckkopplung vor dieser Auswertung
  Lauf 54:
  - `reorganizing` zeigt hÃ¶here Replay-/Distanz-/Neudeutungswerte als
    `carried`
  - Neudeutungsbedarf ist am stÃ¤rksten
  - Reorganisationsgruppe bleibt noch SL-lastig
  NachrÃ¼stung:
  - `open_hypothesis_reorganization_posture` ergÃ¤nzt
  - Haltungen: `reinterpretation_dominant`, `distance_dominant`,
    `replay_dominant`, `low_reorganization_need`

- [ ] Reorganisationshaltung im nÃ¤chsten Lauf prÃ¼fen.
  Ziel:
  - prÃ¼fen, welche Haltung bei `reorganizing` dominiert
  - erst danach mÃ¶gliche Thought-Seed-Reifekopplung entscheiden
  Lauf 55:
  - `reinterpretation_dominant`: `140`, ca. `-59.46` PnL
  - `replay_dominant`: `23`, ca. `+23.19` PnL
  - `distance_dominant`: `0`
  - `low_reorganization_need`: `0`
  Befund:
  - getragene offene Hypothesen sind replay-dominant
  - belastende/reorganisierende offene Hypothesen sind
    reinterpretation-dominant

- [x] Reorganisationshaltung in Thought-Seed-Reifung zurÃ¼ckfÃ¼hren.
  Ziel:
  - `reinterpretation_dominant` als Neudeutungsbedarf sichtbar machen
  - `replay_dominant` als Wiederholungs-/Vertiefungsspur sichtbar machen
  - keine harte Sperre
  - zunÃ¤chst nur innere Diagnose/Meta-Reifung

- [ ] SpÃ¤tere Web-GUI nur als Beobachtungsraum vorbereiten.
  Ziel:
  - erst nach stabilerer Brain-/Backtest-Diagnose umsetzen
  - Konzeptbasis: `GUI_KONSTRUKTION.md`
  - keine GUI-Regeln in die MCM-Entscheidung einbauen

---

# Zuletzt Erledigt

- [x] `MD_ANWEISUNG.md` angelegt.
- [x] `FIX_LISTE.md` bereinigt und auf aktive Punkte reduziert.
- [x] `AKTUELLER_STAND.md` auf kompakten Ist-Zustand reduziert.
- [x] `WICHTIG_MECHANIKEN.md` als technische Mechanik-Schatzkammer neu
  strukturiert.
- [x] Wiederkehrende Unsicherheit als Formfamilie umgesetzt.
- [x] Outcome-Export fÃ¼r neue Formfamilienwerte ergÃ¤nzt.
- [x] Lauf 7/8 als Doppellauf ausgewertet.
- [x] Lauf 9 nach Outcome-Export-Erweiterung ausgewertet.
- [x] `neurochemical_state` als Runtime-/Debug-/Outcome-Schicht umgesetzt.
- [x] `GUI_KONSTRUKTION.md` als Konzept fÃ¼r spÃ¤tere Web-Oberflaeche angelegt.
- [x] Lauf 10 als erster neurochemischer Lauf grob ausgewertet.
- [x] `mcm_neuro_transition_protocol.csv` als automatisches
  `-2/+2` Analyseprotokoll gebaut.
- [x] `sensory_load`-Runtimefehler in `build_perception_state` behoben.
- [x] Erfahrungspaket-Feedback fÃ¼r positive neurochemische Stimulation
  umgesetzt.
- [x] Erfahrungspaket-Labels und `engaged_effort` umgesetzt.
- [x] Pre-Action-Reorganisation umgesetzt.
- [x] Strukturgenaue Pre-Action-Reorganisation umgesetzt.
- [x] Strategische Fensterwahrnehmung diagnostisch umgesetzt.
- [x] `UMSETZUNGSPLAN.md` strukturell bereinigt.
- [x] Debug Lauf 1 mit strategischer Fensterwahrnehmung ausgewertet.
- [x] MCM-Abhandlungen D bis G.1 als TheoriebrÃ¼cke in README,
  UMSETZUNGSPLAN, WICHTIG_MECHANIKEN und MCM_VARIABLEN_MECHANIK
  zusammengefasst.
- [x] Weitere MCM-Theorieanker aus dem MCM-Repository in README,
  UMSETZUNGSPLAN, WICHTIG_MECHANIKEN und MCM_VARIABLEN_MECHANIK
  dokumentiert.
# Aktiver Punkt nach Umsetzung

- [ ] Lauf 56 nach Thought-Seed-Rueckfuehrung auswerten.
  Ziel:
  - pruefen, ob `thought_reifung_direction` sichtbar zwischen
    `replay_maturation`, `distance_maturation` und
    `reinterpretation_maturation` trennt
  - pruefen, ob `seed_reinterpret` bei belastenden offenen Hypothesen erscheint
  - pruefen, ob `seed_replay` bei getragenen offenen Hypothesen als
    Vertiefungsspur erscheint
  - keine harte Handlungssperre ableiten

- [x] Reorganisationshaltung in Thought-Seed-Reifung zurueckfuehren.
  Umsetzung:
  - `last_outcome_decomposition` wird nach Exit/Cancel aus `trade_stats.py` in
    `bot.py` zurueck synchronisiert
  - Meta-Regulation erhaelt die vorherige offene Hypothesenhaltung
  - Thought Seeds erhalten Replay-, Distanz- und Neudeutungspull
  - `mcm_thought_seed_protocol.csv` protokolliert die neuen Reifewerte

---
# Aktiver Punkt - Selbst/Fremd-Differenz

- [ ] Lauf 60 nach RÃ¼ckfÃ¼hrung geliehener Analogie prÃ¼fen.
  Ziel:
  - `borrowed_open_hypothesis_pressure` auswerten
  - prÃ¼fen, ob `borrowed_analogy_watch` + `open_structural_hypothesis`
    weniger Verlustlast erzeugt
  - prÃ¼fen, ob `seed_reinterpret` bei geliehener Analogie hÃ¤ufiger und
    konstruktiver erscheint
  - prÃ¼fen, ob `mixed_translation_zone` weiter positiv bleibt

- [ ] `borrowed_analogy_watch` in Thought-Seed-Reifung zurÃ¼ckfÃ¼hren.
  Ziel:
  - keine harte Sperre
  - geliehene Analogie als unreife semantische Herkunft behandeln
  - besonders bei `open_structural_hypothesis` mehr Reinterpretation,
    Distanz oder Beobachtung erzeugen
  - prÃ¼fen, ob eigene Feldbindung vor Handlung wachsen kann

- [x] `borrowed_analogy_watch` in Thought-Seed-Reifung zurÃ¼ckgefÃ¼hrt.
  Umsetzung:
  - `borrowed_open_hypothesis_pressure`
  - `own_field_binding_pull`
  - weiche VerstÃ¤rkung von Reinterpretation/Distanz
  - Outcome-Export der Thought-Seed-Herkunft ergÃ¤nzt

- [x] Lauf 59 ausgewertet.
  Befund:
  - PnL ca. `+27.40`
  - `borrowed_analogy_watch` im Outcome deutlich negativ: ca. `-22.70`
  - `borrowed_analogy_watch` + `open_structural_hypothesis`:
    `39` FÃ¤lle, `0` TP / `39` SL, ca. `-17.15`
  - `mixed_translation_zone` bleibt positiv: ca. `+36.65`
  - semantische Herkunft hat damit echte diagnostische Aussagekraft

- [ ] Lauf 59 nach direktem Outcome-Export der semantischen Herkunft prÃ¼fen.
  Ziel:
  - PnL/TP/SL nach `semantic_origin_state` auswerten
  - prÃ¼fen, ob `borrowed_analogy_watch` mehr Observe/Reinterpret braucht
  - prÃ¼fen, ob `mixed_translation_zone` produktive Ãœbergangslage ist
  - prÃ¼fen, ob `differentiated_contact` hÃ¤ufiger wird

- [x] Lauf 58 ausgewertet.
  Befund:
  - PnL ca. `+42.74`
  - `semantic_origin_state` verteilt sich erstmals:
    `mixed_translation_zone`, `borrowed_analogy_watch`,
    `unlocated_semantic_contact`, sehr selten `differentiated_contact`
  - bestÃ¤tigte Struktur bleibt 100 % TP-lastig
  - direkter Outcome-Export der semantischen Herkunft wurde nachgerÃ¼stet

- [ ] Lauf 58 auf neue Herkunftsverteilung prÃ¼fen.
  Ziel:
  - Verteilung von `semantic_origin_state` nach weicher Kalibrierung prÃ¼fen
  - neue Margins auswerten:
    `own_vs_foreign_margin`, `borrowed_vs_own_margin`,
    `boundary_support_margin`
  - Zusammenhang mit Observe/Hold/Act und `seed_reinterpret` prÃ¼fen

- [ ] `semantic_origin_state` weicher kalibrieren.
  Ziel:
  - aktuelle Messwerte sind vorhanden, aber alle ZustÃ¤nde landen noch in
    `unlocated_semantic_contact`
  - keine harte IdentitÃ¤tsregel bauen
  - stattdessen organische Lagebeschreibung ermÃ¶glichen:
    `own_field_origin`, `mixed_translation_zone`, `borrowed_analogy_watch`,
    `differentiated_contact`
  - prÃ¼fen, ob `adopted_language_pressure` und
    `self_foreign_boundary_clarity` dafÃ¼r stÃ¤rker relativ zueinander gelesen
    werden mÃ¼ssen

- [x] `semantic_origin_state` weicher kalibriert.
  Umsetzung:
  - relative Margins ergÃ¤nzt
  - ZustÃ¤nde werden nicht mehr nur Ã¼ber hohe harte Einzelwerte bestimmt
  - Protokolle schreiben die neuen Margins mit

- [ ] Lauf 57 prÃ¼fen.
  Ziel:
  - prÃ¼fen, ob die Selbst/Fremd-Spalten jetzt in
    `mcm_field_decision_protocol.csv` und `mcm_memory_thinking_protocol.csv`
    geschrieben werden
  - `semantic_origin_state` auswerten
  - Zusammenhang zwischen `semantic_origin_conflict`, Reflexion und
    Beobachtung prÃ¼fen
  - prÃ¼fen, ob `seed_reinterpret` die offenen Hypothesen in den FolgelÃ¤ufen
    entlastet

- [x] Lauf 57 ausgewertet.
  Befund:
  - PnL ca. `+31.40`
  - Selbst/Fremd-Spalten werden geschrieben
  - `semantic_origin_state` bleibt noch komplett
    `unlocated_semantic_contact`
  - `reinterpretation_maturation` im Outcome positiv mit ca. `+19.25`
  - nÃ¤chster Fix: HerkunftszustÃ¤nde weicher kalibrieren

- [ ] NÃ¤chsten Lauf auf semantische Herkunft prÃ¼fen.
  Ziel:
  - Verteilung von `semantic_origin_state` prÃ¼fen
  - besonders `own_field_origin`, `mixed_translation_zone`,
    `borrowed_analogy_watch` und `unlocated_semantic_contact`
  - prÃ¼fen, ob hoher `semantic_origin_conflict` mit mehr Reflexion,
    Beobachtung oder Neudeutung zusammenfÃ¤llt
  - keine harte IdentitÃ¤tsregel ableiten

- [x] Lauf 56 nach Thought-Seed-RÃ¼ckfÃ¼hrung ausgewertet.
  Befund:
  - PnL ca. `+31.58`
  - `seed_reinterpret` sehr stark sichtbar
  - `reinterpretation_maturation` wirkt bereits als eigene innere Reifespur
  - Selbst/Fremd-Protokollspalten fehlen noch im Lauf-56-CSV und mÃ¼ssen in
    Lauf 57 geprÃ¼ft werden

- [x] Selbst/Fremd-Differenz als MCM-Reifeschicht umgesetzt.
  Umsetzung:
  - Meta-Regulation erhÃ¤lt eigene Herkunfts-/Fremddruckwerte
  - Field- und Memory-Thinking-Protokolle schreiben die neuen Werte
  - Statistik-Kontext Ã¼bernimmt die neuen Werte

---
---

- [x] Lauf 4 nach MCM-Spannungsachse ausgewertet.
  Befund:
  - PnL ca. `+15.69`
  - Long erstmals klar positiv mit ca. `+9.42`
  - Short ebenfalls positiv mit ca. `+6.27`
  - `mcm_field_decision_protocol.csv` schreibt die neuen Achsvariablen jetzt
    sauber mit
  - `mcm_axis_state` bleibt fast vollstaendig bei `0`
  - keine sichtbare `positive_zero_point_regulation`, also keine starke
    positive Ueberdehnung

- [ ] Lauf 5 nach MCM-Spannungsachse pruefen.
  Ziel:
  - pruefen, ob Long-Stabilisierung aus Lauf 4 wiederholbar ist
  - `positive_overextension` vor schlechten Long-Entscheidungen auswerten
  - `mcm_axis_state`, `mcm_axis_tension` und `positive_return_pressure` nach
    Long/Short/Wait vergleichen
  - keine harte Regel ableiten, sondern nur organische Spannungsfuehrung
    schaerfen

- [x] Gedanken-Verdauung fuer offene Hypothesen umgesetzt.
  Umsetzung:
  - `thought_digestive_replay_pull`
  - `thought_digestive_distance_pull`
  - `thought_digestive_integration_pull`
  - `thought_digestive_returned_trust`
  - `thought_digest_state`
  - Thought-Memory speichert die Werte fuer Seeds und Familien
  - Thought-Seed-Protokoll und Trade-Stats schreiben die Werte mit
  - Compile-Pruefung bestanden

- [ ] Naechsten Lauf auf Hypothesen-Verdauung pruefen.
  Ziel:
  - Verteilung von `thought_digest_state` auswerten
  - pruefen, ob `open_hypothesis_reorganizing_memory` eher in Replay,
    Abstand oder Integration geht
  - pruefen, ob `digestive_trust_return` vor besseren Entscheidungen sichtbar
    wird
  - keine harte Sperre ableiten, sondern weiche Reifung und innere
    Nachverarbeitung schaerfen

- [x] Lauf 11 und Lauf 12 nach Gedanken-Verdauung geprueft.
  Befund:
  - Lauf 11 im sichtbaren Debug staerker Long-getragen
  - Lauf 12 staerker Short-verteilt und im Endzustand niedrigerer Cortisolwert
  - beide enden bei `open_hypothesis_reorganizing_memory`
  - Thought-Memory zeigt bereits `digestive_replay` und `digestive_distance`
  - `digestive_trust_return` ist noch nicht stabil sichtbar

- [ ] Gezieltes Thought-Seed-Debug fuer reduzierte Debug-Ausgabe bauen.
  Ziel:
  - keine Rueckkehr zur kompletten CSV-Flut
  - kleine Diagnose-Datei fuer `thought_digest_state`,
    `thought_reifung_direction`, `thought_digestive_replay_pull`,
    `thought_digestive_distance_pull`, `thought_digestive_integration_pull`,
    `thought_digestive_returned_trust`, `open_hypothesis_reifung_state`,
    `open_hypothesis_action_permission` und `open_hypothesis_reality_check_need`
  - damit sichtbar machen, wann DIO replayt, Abstand nimmt, integriert oder
    Vertrauen zurueckbekommt

- [x] Gezieltes Thought-Digest-Debug umgesetzt.
  Umsetzung:
  - neue Datei `core/mcm_thought_digest_protocol.csv`
  - `DIO_CORE_DEBUG` schreibt nicht mehr die grosse
    `mcm_thought_seed_protocol.csv`
  - Thought-Memory bleibt aktiv
  - Research-/GUI-Profile koennen weiterhin die grosse Thought-Seed-Datei
    schreiben
  - Compile-Pruefung bestanden

- [ ] Naechsten Lauf mit bestehender Erfahrung auf anderem Datensatz pruefen.
  Vorschlag:
  - `data/1-12_2025_5m_SOLUSDT.csv`
  - Memory behalten, damit Transfer sichtbar wird
  - danach `core/mcm_thought_digest_protocol.csv` auswerten
  - besonders `digestive_replay`, `digestive_distance`,
    `digestive_integration`, `digestive_trust_return`, Cortisol und
    `open_hypothesis_action_permission` vergleichen

- [x] Lauf 13 mit Thought-Digest-Protokoll ausgewertet.
  Befund:
  - PnL ca. `+35.43`
  - Long ca. `+4.09`, Short ca. `+31.34`
  - neue Datei `core/mcm_thought_digest_protocol.csv` wird geschrieben
  - grosse `mcm_thought_seed_protocol.csv` wird im DIO-Core-Profil nicht mehr
    geschrieben
  - `digestive_replay`: `3776`
  - `digestive_distance`: `679`
  - `digestive_trust_return`: noch `0`
  - `open_hypothesis_reorganizing_memory` wird sauber in Replay/Abstand
    verschoben statt direkt handlungsnah zu bleiben

- [ ] Trust-Return-Vorstufen aus Lauf 13 pruefen.
  Ziel:
  - Zeilen mit `thought_digestive_returned_trust >= 0.25` untersuchen
  - pruefen, ob diese spaeter bessere Entscheidungen, niedrigeren Cortisolwert
    oder hoeheren `open_hypothesis_action_permission` vorbereiten
  - keine harte Schwelle bauen, sondern Rueckkehr von Vertrauen organischer
    sichtbar machen

- [x] Trust-Return-Vorstufe umgesetzt.
  Umsetzung:
  - `trust_return_readiness` ergaenzt
  - neuer Zustand `digestive_trust_emergence`
  - `digestive_trust_return` muss nicht mehr gegen Replay/Distance gewinnen,
    sondern darf waehrend innerer Verarbeitung entstehen
  - Thought-Memory, Thought-Digest-Protokoll und Trade-Stats schreiben die
    neue Readiness mit
  - Compile-Pruefung bestanden

- [ ] Naechsten Lauf auf Trust-Return pruefen.
  Ziel:
  - Verteilung von `digestive_trust_emergence` und `digestive_trust_return`
    pruefen
  - `trust_return_readiness` gegen Cortisol, Action-Permission und spaetere
    Tradequalitaet lesen
  - pruefen, ob Vertrauen zurueckkehrt, ohne dass DIO zu frueh motorisch wird

- [x] Lauf 14 bis Lauf 16 nach Trust-Return ausgewertet.
  Befund:
  - `digestive_trust_emergence` taucht stabil auf:
    Lauf 14 `39`, Lauf 15 `31`, Lauf 16 `34`
  - `digestive_trust_return` taucht erstmals auf:
    Lauf 14 `5`, Lauf 15 `3`, Lauf 16 `3`
  - Trust-Return entsteht fast immer aus `open_hypothesis_carried_memory` und
    `replay_maturation`
  - haeufige Kopplung an `act`
  - Cortisol ist dabei nicht niedrig; Vertrauen ist also noch motorisch
    angespannt

- [x] Trust-Return von direkter Motorik feiner entkoppeln.
  Ziel:
  - keine Handlungssperre bauen
  - `digestive_trust_emergence` als Stabilisierung / Fokussierung lesen
  - wenn Trust zurueckkommt, aber Cortisol noch hoch ist, soll DIO Vertrauen
    halten, replayen oder fokussieren koennen
  - erst wenn Vertrauen und Nervensystem zusammen tragfaehig wirken, soll die
    Motorik daraus natuerlich mehr Handlungskraft bekommen
  Umsetzung:
  - `trust_return_motor_heat`
  - `trust_return_stabilization_need`
  - `trust_return_focus_pull`
  - `trust_return_motor_mode`
  - vorheriger Digest-Zustand wird als Nachhall in die Meta-Regulation
    aufgenommen
  - bei hohem Trust-Return und hoher nervlicher Last wird nicht hart
    blockiert, sondern in `act_watch`, `replan`, Replay oder Fokussierung
    verschoben
  - Thought-Digest-Protokoll und Trade-Stats schreiben die neue Schicht mit
  - Compile-Pruefung bestanden

- [ ] Naechsten Lauf auf Trust-Return-Motorik pruefen.
  Ziel:
  - Verteilung von `trust_return_motor_mode` pruefen
  - besonders `trust_stabilize_before_act`, `trust_focused_ready` und
    `trust_emerging` lesen
  - pruefen, ob `digestive_trust_emergence` seltener direkt in `act` kippt
  - Cortisol, MaxDD, PnL-Verlauf und offene Hypothesenlast vergleichen
  - wichtig: keine Sperrlogik ableiten, sondern schauen, ob DIO Vertrauen
    erst stabilisieren kann, bevor es motorisch wirkt

- [x] Lauf 17 nach Trust-Return-Motorik geprueft.
  Befund:
  - Netto-PnL ca. `+30.44`
  - Trades `378`, TP/SL `158/220`
  - Long ca. `-2.34`, Short ca. `+32.78`
  - Max-DD ca. `5.58%`
  - `digestive_trust_emergence`: `28`
  - `digestive_trust_return`: `4`
  - `trust_focused_ready`: `32`
  - `trust_stabilize_before_act`: `0`
  - die Entkopplung ist sichtbar, aber noch eher als Fokus-Schicht statt als
    echte Stabilisierung vor Handlung

- [x] Trust-Return-Stabilisierung organischer speisen.
  Ziel:
  - keine harte Sperre und kein mechanisches Absenken als Blocker
  - `trust_return_stabilization_need` weicher aus Cortisol,
    offener Hypothesenlast, niedriger Innen/Aussen-KohÃ¤renz und
    `digestive_trust_emergence` speisen
  - DIO soll Vertrauen halten und prÃ¼fen kÃ¶nnen, ohne es sofort motorisch zu
    entladen
  - naechster Lauf muss zeigen, ob `trust_stabilize_before_act` natuerlich
    auftaucht und ob offene reorganisierende Hypothesen weniger Schaden machen
  Umsetzung:
  - `trust_return_open_hypothesis_load`
  - `trust_return_context_instability`
  - beide Werte speisen `trust_return_motor_heat`,
    `trust_return_stabilization_need` und leicht den Fokus-Pull
  - Thought-Digest-Protokoll und Trade-Stats schreiben die neuen Werte mit

- [ ] Naechsten Lauf nach organischer Trust-Stabilisierung pruefen.
  Ziel:
  - pruefen, ob `trust_stabilize_before_act` jetzt natuerlich auftaucht
  - direkte Kopplung `digestive_trust_emergence -> act` beobachten
  - offene reorganisierende Hypothesen nach PnL/SL-Last pruefen
  - `trust_return_open_hypothesis_load` und
    `trust_return_context_instability` gegen Cortisol und
    `inner_outer_alignment` lesen

- [x] Lauf 18 nach organischer Trust-Stabilisierung geprueft.
  Befund:
  - Netto-PnL ca. `+24.43`
  - Trades `352`, TP/SL `144/208`
  - Long ca. `+8.46`, Short ca. `+15.97`
  - Max-DD ca. `6.94%`
  - `trust_stabilize_before_act` taucht erstmals auf: `11`
  - `trust_focused_ready`: `13`
  - direkte Kopplung `digestive_trust_emergence -> act` sinkt:
    Lauf 17 `19/28`, Lauf 18 `11/22`
  - Stabilisierung ist sichtbar, aber noch vor allem in Observe/Hold, nicht
    als aktive Umleitung aus geplanter Motorik

- [x] Trust-Stabilisierung an Motorik-Schnittstelle feiner anbinden.
  Ziel:
  - keine Sperre bauen
  - wenn `trust_stabilize_before_act` bei geplanter Handlung auftaucht, DIO
    eher in `act_watch` oder kurzes Replay verschieben lassen
  - DIO soll Vertrauen als innere Information halten koennen, bevor Handlung
    daraus wird
  - pruefen, ob offene reorganisierende Hypothesen dadurch weniger teuer
    werden, ohne bestaetigte Strukturdeutung zu bremsen
  Umsetzung:
  - `trust_return_motor_contact_strength`
  - `trust_return_act_bridge`
  - `previous_confirmed_structure_protection`
  - bestaetigte Strukturdeutung bekommt Schutz vor unnÃ¶tiger DÃ¤mpfung
  - Trust-Stabilisierung kann geplante Handlung weich in `act_watch` oder
    Replay verschieben, wenn die innere Lage noch nicht trÃ¤gt

- [ ] Naechsten Lauf auf Trust-Motorik-Bruecke pruefen.
  Ziel:
  - `trust_return_act_bridge` bei geplanten Handlungen lesen
  - zaehlen, wie oft daraus `act_watch` oder `replan` entsteht
  - bestaetigte Strukturdeutung weiter auf TP/SL und PnL pruefen
  - offene reorganisierende Hypothesen auf SL-Last und PnL pruefen
  - PnL, Max-DD und Long/Short-Verteilung vergleichen

- [x] Diagnose zur schwachen ersten Laufhaelfte im alten Datensatz erstellt.
  Befund:
  - viele Laeufe bauen den groessten PnL erst nach ca. 50 Prozent auf
  - das Muster war nicht erst durch die letzte Trust-Bruecke vorhanden
  - alter Datensatz hat stark unterschiedliche Viertel:
    0-25 Prozent Push, 25-50 Prozent Abverkauf, 50-75 Prozent massiver
    Abverkauf, 75-100 Prozent seitwaerts
  - DIO sortiert in der ersten Haelfte offenbar Regimewechsel und offene
    Hypothesen; spaeter wird besonders Short tragender

- [ ] Neuen Datensatz gegen 50-Prozent-Muster testen.
  Ziel:
  - `3-4_2026_5m_SOLUSDT.csv` mit bestehender Erfahrung laufen lassen
  - pruefen, ob der schwache erste-Haelfte-Effekt wieder auftaucht
  - wenn ja: Ursache eher Denk-/Motorikarchitektur
  - wenn nein: Ursache eher alter Datensatz / Regimeuebergang
  - dabei `trust_return_act_bridge`, offene Hypothesenlast,
    bestaetigte Strukturdeutung und Long/Short-Profil vergleichen

- [x] Ersten Transferlauf auf `3-4_2026_5m_SOLUSDT.csv` geprueft.
  Befund:
  - Debug: `debug_lauf_21`
  - Netto-PnL ca. `-17.29`
  - Trades `277`, TP/SL `81/196`
  - Long ca. `-5.80`, Short ca. `-11.50`
  - Max-DD ca. `17.69%`
  - bestaetigte Strukturdeutung bleibt stark:
    `30 TP / 0 SL`, ca. `+24.43`
  - offene Strukturhypothese und low-Strukturen fressen den Lauf:
    offene Hypothese ca. `-34.45`, low ca. `-46.78`
  - alter Short-Vorteil traegt auf neuem Datensatz nicht

- [ ] Transfer-/Fremdheitsregulation vorbereiten.
  Ziel:
  - keine alte Erfahrung loeschen
  - keine harte Long-/Short-/Low-Regel bauen
  - alte Erfahrung auf fremdem Datensatz erst als Hypothese behandeln
  - lokale Bestaetigung muss Handlungskraft reifen lassen
  - bestaetigte Strukturdeutung schuetzen
  - offene Hypothesen und low-Strukturen auf fremdem Boden eher beobachten,
    replayen, nachreifen lassen

- [ ] Vergleichslauf mit frischer Memory auf neuem Datensatz pruefen.
  Ziel:
  - erkennen, ob der Transferbruch aus alter Erfahrung stammt
  - gleicher Datensatz `3-4_2026_5m_SOLUSDT.csv`
  - Memory frisch aufbauen
  - PnL, Long/Short, confirmed/open/low und Thought-Memory vergleichen

- [x] Lauf 22 mit frischer Memory auf neuem Datensatz geprueft.
  Befund:
  - Netto-PnL ca. `-18.41`
  - Trades `337`, TP/SL `100/237`
  - Long ca. `-9.24`, Short ca. `-9.17`
  - Max-DD ca. `19.26%`
  - frische Memory ist nicht besser als bestehende Erfahrung
  - bestaetigte Strukturdeutung bleibt stark:
    `26 TP / 0 SL`, ca. `+21.15`
  - low, offene Hypothese und reorganisierende Hypothese bleiben die
    Hauptverlusttraeger

- [ ] Moeglichkeitsreife / Possibility-Maturity vorbereiten.
  Ziel:
  - DIO darf Moeglichkeiten weiter sehen
  - Moeglichkeiten sollen nicht hart verboten werden
  - offene Moeglichkeit braucht lokale Bestaetigung, Strukturkontakt,
    Wiedererkennung oder Replay, bevor sie Motorik bekommt
  - bestaetigte Strukturdeutung schuetzen
  - low/open/reorganizing nicht pauschal blockieren, sondern als unreife
    Moeglichkeit in Beobachtung/Reifung halten

- [x] Erste Possibility-Maturity-Schicht umgesetzt.
  Befund:
  - nicht ausgefuehrte Hypothesen werden weiter beobachtet
  - aus `missed_gain`, `saved_loss` und `neutral` entsteht ein
    beobachteter Hypothesen-Ausgang
  - neue Felder:
    `hypothesis_observed_outcome`,
    `hypothesis_confirmation_without_action`,
    `hypothesis_rejection_without_action`,
    `hypothesis_observation_maturity`,
    `possibility_maturity`,
    `possibility_caution`,
    `possibility_action_support`,
    `possibility_reality_check_need`
  - Wirkung ist weich:
    bestaetigte Moeglichkeiten erhalten etwas mehr Handlungssupport,
    belastende Moeglichkeiten erzeugen eher Realitaetspruefung,
    Beobachtung oder Replan-Druck
  - keine harte Sperre, keine Long/Short-Regel, keine Low-Blockade

- [ ] Naechsten Debug-Lauf nach Possibility-Maturity pruefen.
  Ziel:
  - pruefen, ob offene Hypothesen weniger blind motorisch werden
  - pruefen, ob `confirmed_structural_interpretation` weiter geschuetzt bleibt
  - besonders lesen:
    `hypothesis_observed_outcome`,
    `possibility_maturity`,
    `possibility_action_support`,
    `possibility_reality_check_need`

- [x] Hypothesen-Vertrauensschicht umgesetzt.
  Ziel:
  - DIO lernt nicht nur Beobachtung, sondern Vertrauen aus bestaetigten
    Hypothesen
  - keine starre Trefferquote, sondern weiche synaptische Gewichtung
  - bestaetigte Hypothesen bekommen mehr Prioritaet
  - belastende Hypothesen erzeugen Frust-/Distanz-/Replan-Druck
  - neue Felder:
    `hypothesis_trust_score`,
    `hypothesis_trust_priority`,
    `hypothesis_frustration_risk`,
    `hypothesis_distance_risk`,
    `hypothesis_trust_state`,
    `dominant_hypothesis_trust_key`,
    `dominant_hypothesis_trust_score`

- [ ] Naechsten Lauf nach Hypothesen-Vertrauen pruefen.
  Ziel:
  - steigt `hypothesis_trust_priority` bei tragenden Hypothesen?
  - entsteht bei schlechter Hypothesenbilanz `hypothesis_frustration_risk`?
  - wird DIO dadurch gezielter, ohne offene Varianz hart zu blockieren?

- [x] Lauf 23 nach Hypothesen-Vertrauen geprÃ¼ft.
  Befund:
  - Netto-PnL ca. `-26.34`
  - `confirmed_structural_interpretation` bleibt stark:
    `15 TP / 0 SL`, ca. `+12.79`
  - `open_hypothesis_carried` bleibt stark:
    `27 TP / 0 SL`, ca. `+21.19`
  - HauptschÃ¤den:
    `low` ca. `-37.30`,
    `open_hypothesis_reorganizing` ca. `-37.30`,
    `open_structural_hypothesis` ca. `-20.06`
  - globale Beobachtungsbilanz ist fast 50/50:
    `missed_gain` ca. `2090`,
    `saved_loss` ca. `2169`
  - dadurch bleibt globales Vertrauen niedrig:
    `hypothesis_trust_score` ca. `0.157`,
    `hypothesis_trust_priority` ca. `0.166`
  - einzelne Formfamilien zeigen aber hohes lokales Vertrauen
    bis ca. `0.67`

- [ ] Lokales Hypothesenvertrauen anbinden.
  Ziel:
  - globales Vertrauen nur als Hintergrundton verwenden
  - aktuelle `form_symbol_id` / Formfamilie gegen
    `hypothesis_trust_families` spiegeln
  - lokale BestÃ¤tigung soll Handlungssupport erhÃ¶hen
  - fehlende lokale BestÃ¤tigung bei `open_hypothesis_reorganizing` soll
    Distanz, Replay oder Replan erhÃ¶hen
  - keine harte Sperre, keine feste Trefferquote

- [ ] Hypothesen-Vertrauenswerte in passendem Core-Protokoll sichtbar machen.
  Ziel:
  - `hypothesis_trust_score`
  - `hypothesis_trust_priority`
  - `hypothesis_frustration_risk`
  - `hypothesis_distance_risk`
  - `hypothesis_trust_state`
  - `dominant_hypothesis_trust_key`

- [x] Projektstruktur Phase 1 angelegt.
  Befund:
  - neue Pakete:
    `core/`, `trading/`, `memory/`, `debug_tools/`, `docs/documente/`
  - Module sind aktuell sichere Adapter
  - bestehende Imports bleiben stabil
  - Importtest erfolgreich
  - Struktur dokumentiert in `docs/06_struktur/PROJEKTSTRUKTUR.md`
  - `debug/` bleibt Runtime-Ausgabeordner, Code liegt in `debug_tools/`

- [ ] Refactoring Phase 2: Debug-Code auslagern.
  Ziel:
  - `debug_reader.py` schrittweise nach `debug_tools/writers.py` und
    `debug_tools/protocols.py` aufteilen
  - zuerst Schreibpfade und Buffer-Logik
  - danach Protokollgruppen
  - keine Ã„nderung an Debug-Ausgabepfaden

- [x] Refactoring Phase 2a: Debug-Writer ausgelagert.
  Befund:
  - Schreib-/Pfad-/Buffer-Schicht liegt in `debug_tools/writers.py`
  - `debug_reader.py` bleibt KompatibilitÃ¤ts-Wrapper
  - bestehende Imports bleiben stabil
  - `py_compile` und Importtest erfolgreich
  - Debug-Probe erfolgreich, Probeordner entfernt

- [x] Refactoring Phase 3: Thought-Memory-Store-Grenze bereinigt.
  Befund:
  - `_thought_memory_*` liegt nicht mehr als Kopie in `MCM_Brain_Modell.py`
  - Implementierung liegt in `core/thought_memory.py`
  - Speicher-/Persistenzzugriff laeuft ueber `memory/thought_memory_store.py`
  - `bot.py`, `debug_tools/protocols.py` und `core/form_language.py` nutzen
    jetzt den Store-Adapter statt direkter Core-Kopplung
  - Importtest, Runtime-Queue-Smoke, Zieltests, kompletter Testlauf und
    breiter Compile erfolgreich

- [ ] Varianzverengung / mechanische Schutzkonvergenz prÃ¼fen.
  Ziel:
  - keine einzelne Schutzschicht vorschnell entfernen
  - prÃ¼fen, ob mehrere weiche Regulatoren zusammen wie ein harter Reflex
    wirken
  - besonders beobachten:
    `zero_point_regulation`, `context_cluster_negative`,
    `trust_return_act_bridge`, `open_hypothesis_reifung_state`,
    `observe`, `hold`, `act_watch`, `act`
  - Varianz nicht kÃ¼nstlich erhÃ¶hen, sondern Beweglichkeit im MCM-Feld
    zurÃ¼ckgeben
  - organisches Ziel:
    Schutz darf vorhanden sein, aber nicht zur regulatorischen Starre werden

- [x] Runtime-Smoke-Fix: `build_strategic_window_state` wiederhergestellt.
  Befund:
  - direkter `step_mcm_runtime` brach nach der Refactoring-Stabilisierung mit
    fehlender Strategic-Window-Bruecke ab
  - Funktion wieder in `MCM_Brain_Modell.py` eingefuegt
  - Lookback-Bereiche liefern wieder `area_focus_candidates`,
    `area_bearing_quality`, `area_order_intention`, Replay-/Timing- und
    Raumzeit-Fit
  - direkter Runtime-Smoke mit echten CSV-Daten erfolgreich
  - Zieltests, kompletter Testlauf und breiter Compile erfolgreich

- [ ] Threaded-Bot-Smoke / Followup-Pfad auf Blockade pruefen.
  Befund:
  - ein kleiner Bot-Smoke lief nicht sauber durch und musste beendet werden
  - direkte Brain-Runtime funktioniert, daher liegt der naechste Verdacht eher
    bei Runtime-Thread, Debug-Flush, Followup oder Bot-Orchestrierung
  Ziel:
  - kurzen Bot-Pfad mit reduziertem Debug erneut kontrollieren
  - unterscheiden zwischen Brain-Rechenzeit und Bot-/Debug-Wartezeit

- [x] Runtime-Thread gegen endloses Blockieren abgesichert.
  Befund:
  - `stop_runtime_thread()` und Queue-Idle-Warten hatten vorher keine harte
    Diagnosegrenze
  - dadurch konnte ein Smoke-Test bei einem haengenden Pfad den Prozess
    blockieren
  Umsetzung:
  - `MCM_RUNTIME_THREAD_STOP_TIMEOUT_SECONDS`
  - `MCM_RUNTIME_QUEUE_IDLE_TIMEOUT_SECONDS`
  - Watchdog-Protokoll `runtime_thread_watchdog.csv`
  Ergebnis:
  - Thread-Start/Stop-Smoke erfolgreich
  - Queue-Smoke mit 3 Marktfenstern erfolgreich
  - Zieltests, kompletter Testlauf und breiter Compile erfolgreich

- [x] Debug-Writer-Grenze bereinigt.
  Befund:
  - mehrere interne Module nutzten noch den alten Root-Wrapper
    `debug_reader.py`
  - Debug-Schreiblogik liegt aber in `debug_tools/writers.py`
  Umsetzung:
  - interne Debug-, Memory-, Core-, Gate- und Stats-Module importieren jetzt
    direkt aus `debug_tools.writers`
  - Root-/Runtime- und API-nahe Einstiegspunkte bleiben vorerst auf dem
    Kompatibilitaetswrapper
  Geprueft:
  - Importtest erfolgreich
  - Runtime-Queue-Smoke erfolgreich
  - Zieltests, kompletter Testlauf und breiter Compile erfolgreich

- [x] Formsymbol-Orchestrierung ausgelagert.
  Befund:
  - die Einzelbausteine der Formsprache lagen bereits in `core/form_language.py`
  - der Speicher lag bereits in `memory/form_symbol_memory.py`
  - `MCM_Brain_Modell.py` enthielt noch den grossen Zustandsaufbau und das
    Outcome-Lernen der Formzeichen
  Umsetzung:
  - `core/form_symbol_orchestration.py` angelegt
  - `build_form_symbol_state` verschoben
  - `update_form_symbol_development_from_outcome` verschoben
  - Brain behaelt Kompatibilitaetswrapper
  Geprueft:
  - direkter Runtime-Smoke baut Formsymbol
  - Runtime-Queue-Smoke erfolgreich
  - Zieltests, kompletter Testlauf und breiter Compile erfolgreich

- [x] Runtime-Entry Meta-Bruecken gekapselt.
  Befund:
  - `_compute_runtime_entry_result` enthielt Review-Feedback- und
    MCM-Kontakt-Meta-Anbindung direkt im grossen Ablauf
  - diese Abschnitte sind reine Zustandsuebertragung und damit gut
    auslagerbar
  Umsetzung:
  - `core/runtime_entry.py` angelegt
  - `apply_review_feedback_to_meta` ausgelagert
  - `apply_strategic_window_to_meta` ausgelagert
  - `apply_active_mcm_contact_to_meta` ausgelagert
  - `commit_runtime_entry_bot_state` ausgelagert
  - `record_runtime_entry_rejection_protocol` ausgelagert
  - `synchronize_entry_choice_prices` ausgelagert
  - `synchronize_entry_choice_result` ausgelagert
  - `build_virtual_observation_plan` ausgelagert
  - `build_runtime_no_plan_result` ausgelagert
  - `build_runtime_entry_trade_result` ausgelagert
  - `record_runtime_entry_result_protocol` ausgelagert
  - `build_runtime_field_metrics` ausgelagert
  - `resolve_runtime_external_perception` ausgelagert
  - `build_runtime_perception_stack` ausgelagert
  - `build_runtime_affective_symbol_stack` ausgelagert
  - `build_runtime_temporal_context_stack` ausgelagert
  - `build_runtime_cognitive_regulation_stack` ausgelagert
  - `build_runtime_contact_regulation_stack` ausgelagert
  Geprueft:
  - gezielter `py_compile` erfolgreich
  - direkter Runtime-Smoke erfolgreich
  - direkter External-Perception-Smoke erfolgreich
  - direkter Perception-Stack-Smoke erfolgreich
  - direkter Affective-Symbol-Stack-Smoke erfolgreich
  - direkter Temporal-Context-Stack-Smoke erfolgreich
  - direkter Cognitive-Regulation-Stack-Smoke erfolgreich
  - Zieltests, kompletter Testlauf und breiter Compile erfolgreich

- [x] Bot-Market-Packet-Helfer ausgelagert.
  Befund:
  - `bot.py` enthielt noch technische Helfer fuer Market-Window-Normalisierung,
    Runtime-Packet-Aufbau und Live-Packet-Key
  - diese Logik gehoert zur Bot-Orchestrierung, nicht zum MCM-Kern
  Umsetzung:
  - `bot_engine/market_packets.py` angelegt
  - `_normalize_market_window` delegiert an `normalize_market_window`
  - `_build_outer_market_state_packet` delegiert an
    `build_outer_market_state_packet`
  - `_build_runtime_market_packet` delegiert an `build_runtime_market_packet`
  - `_build_live_market_packet_key` delegiert an `build_live_market_packet_key`
  Geprueft:
  - gezielter `py_compile` erfolgreich
  - Bot-Persistence-/Gate-Zieltests erfolgreich
  - kompletter Testlauf erfolgreich
  - breiter Python-Compile erfolgreich
  - kompletter Testlauf erfolgreich
  - breiter Python-Compile erfolgreich
  - kompletter Testlauf erfolgreich
  - breiter Python-Compile erfolgreich
  - direkter Market-Packet-Smoke erfolgreich

- [x] Idle-Thinking-Protokoll ausgelagert.
  Befund:
  - `bot.py` enthielt eine grosse Debug-Schreibfunktion fuer
    `mcm_idle_thinking_protocol.csv`
  - diese Funktion ist Diagnoseausgabe und keine MCM-Entscheidungsmechanik
  Umsetzung:
  - `bot_engine/idle_thinking_protocol.py` angelegt
  - `_write_idle_thinking_protocol` delegiert an das neue Modul
  Geprueft:
  - gezielter `py_compile` erfolgreich
  - Bot-Persistence-/Gate-Zieltests erfolgreich
  - kompletter Testlauf erfolgreich
  - breiter Python-Compile erfolgreich

- [x] Visual-Cortex-Protokoll ausgelagert.
  Befund:
  - `bot.py` enthielt eine weitere Debug-Schreibfunktion fuer
    `mcm_visual_cortex_protocol.csv`
  - die Funktion protokolliert bestehende visuelle Wahrnehmung, bewertet sie
    aber nicht neu
  Umsetzung:
  - `bot_engine/visual_cortex_protocol.py` angelegt
  - `_record_visual_cortex_protocol` delegiert an das neue Modul
  Geprueft:
  - gezielter `py_compile` erfolgreich
  - Bot-Persistence-/Gate-Zieltests erfolgreich
  - kompletter Testlauf erfolgreich
  - breiter Python-Compile erfolgreich

- [x] Runtime-Action-Context ausgelagert.
  Befund:
  - `bot.py` enthielt mehrere technische Helfer fuer Action-Kontext,
    Runtime-Payload und Timestamp-State
  - diese Helfer bereiten Ausfuehrung vor, entscheiden aber nicht selbst
  Umsetzung:
  - `bot_engine/action_context.py` angelegt
  - Action-Context-Methoden in `bot.py` delegieren an das neue Modul
  Geprueft:
  - gezielter `py_compile` erfolgreich
  - Bot-Persistence-/Gate-Zieltests erfolgreich
  - kompletter Testlauf erfolgreich
  - breiter Python-Compile erfolgreich

- [x] Runtime-Taktung ausgelagert.
  Befund:
  - `bot.py` enthielt technische Berechnung fuer dynamische Last,
    Idle-Schlafzeit, Idle-Zyklen und Market-Followup-Zyklen
  - diese Funktionen steuern Taktung, enthalten aber keine neue Entscheidung
  Umsetzung:
  - `bot_engine/runtime_timing.py` angelegt
  - Runtime-Taktungs-Methoden in `bot.py` delegieren an das neue Modul
  Geprueft:
  - gezielter `py_compile` erfolgreich
  - Bot-Persistence-/Gate-Zieltests erfolgreich
  - kompletter Testlauf erfolgreich
  - breiter Python-Compile erfolgreich

- [x] Feed-/Runtime-Loop-Orchestrierung ausgelagert.
  Befund:
  - `bot.py` enthielt technische Loop-/Feed-Helfer fuer Runtime-Thread,
    Feed-Fenster und Market-Followup
  - diese Funktionen steuern Ablauf, enthalten aber keine neue
    Wahrnehmungs- oder Entscheidungsmechanik
  Umsetzung:
  - `bot_engine/feed_runtime.py` angelegt
  - Feed-/Loop-Methoden in `bot.py` delegieren an das neue Modul
  Geprueft:
  - gezielter `py_compile` erfolgreich
  - Bot-Persistence-/Gate-Zieltests erfolgreich
  - kompletter Testlauf erfolgreich
  - breiter Python-Compile erfolgreich

- [x] Market-Perception-Aufbau ausgelagert.
  Befund:
  - `bot.py` enthielt noch den technischen Aufbau der Market-Perception-
    Komponenten und eine aeussere Temporal-Perception-Bruecke
  - diese Logik gehoert fachlich zur Bot-Engine-Wahrnehmungsbruecke
  Umsetzung:
  - `bot_engine/market_perception.py` angelegt
  - Market-Perception-Methoden in `bot.py` delegieren an das neue Modul
  Geprueft:
  - gezielter `py_compile` erfolgreich
  - Bot-Persistence-/Gate-Zieltests erfolgreich
  - kompletter Testlauf erfolgreich
  - breiter Python-Compile erfolgreich

- [x] Runtime-Processing ausgelagert.
  Befund:
  - `bot.py` enthielt Runtime-Adapter fuer resolved Market-Packets,
    `step_mcm_runtime`, Seeding und Finalisierung
  - diese Logik ist Bruecken-/Orchestrierungscode, nicht der Brain-Kern
  Umsetzung:
  - `bot_engine/runtime_processing.py` angelegt
  - Runtime-Processing-Methoden in `bot.py` delegieren an das neue Modul
  Geprueft:
  - gezielter `py_compile` erfolgreich
  - Bot-Persistence-/Gate-Zieltests erfolgreich
  - kompletter Testlauf erfolgreich
  - breiter Python-Compile erfolgreich

- [x] Execution-Path-Wrapper ausgelagert.
  Befund:
  - `bot.py` enthielt duenne Wrapper fuer die Reihenfolge Position, Pending,
    neue Entry-Entscheidung
  - die eigentlichen Handler bleiben wegen hoher Zustandskopplung vorerst im
    Bot
  Umsetzung:
  - `bot_engine/execution_paths.py` angelegt
  - Runtime-Execution-Path-Methoden in `bot.py` delegieren an das neue Modul
  Geprueft:
  - gezielter `py_compile` erfolgreich
  - Bot-Persistence-/Gate-Zieltests erfolgreich
  - kompletter Testlauf erfolgreich
  - breiter Python-Compile erfolgreich

- [x] Runtime-Action-Cycle in Action-Context erweitert ausgelagert.
  Befund:
  - `bot.py` enthielt noch Adapter fuer Runtime-Execution-Payload,
    Action-Kontext-Vorbereitung und Action-Cycle-Start
  Umsetzung:
  - `bot_engine/action_context.py` erweitert
  - weitere Action-Context-Methoden in `bot.py` delegieren an das Modul
  Geprueft:
  - gezielter `py_compile` erfolgreich
  - Bot-Persistence-/Gate-Zieltests erfolgreich
  - kompletter Testlauf erfolgreich
  - breiter Python-Compile erfolgreich

- [x] Execution-Outcome-Helfer ausgelagert.
  Befund:
  - `bot.py` enthielt Abschlusslogik fuer Pending-Fill, Non-Action,
    Position-Cancel/-Resolution und Entry-Attempt-Abschluss
  - diese Helfer schreiben bestehende State-/Stats-/Memory-/Episode-Punkte,
    erzeugen aber keine neue Entscheidung
  Umsetzung:
  - `bot_engine/execution_outcomes.py` angelegt
  - Finalize-/Outcome-Methoden in `bot.py` delegieren an das neue Modul
  Geprueft:
  - gezielter `py_compile` erfolgreich
  - Bot-Persistence-/Gate-Zieltests erfolgreich
  - kompletter Testlauf erfolgreich
  - breiter Python-Compile erfolgreich

- [x] Bot-Memory-Save-Wrapper ausgelagert.
  Befund:
  - `bot.py` enthielt noch den Bot-spezifischen Save-Wrapper fuer
    Formsymbol-/Thought-Memory-Flush und `memory_state.json`
  Umsetzung:
  - `memory/memory_state.py` um `save_bot_memory_state` erweitert
  - `_save_memory_state` in `bot.py` delegiert an den Memory-Bereich
  Geprueft:
  - gezielter `py_compile` erfolgreich
  - Bot-Persistence-/Gate-Zieltests erfolgreich
  - kompletter Testlauf erfolgreich
  - breiter Python-Compile erfolgreich

- [x] Regulationspfad gegen alten Funktionsstand abgeglichen.
  Befund:
  - `allow_plan`-AuslÃ¶ser und RÃ¼cknahmen sind im aktuellen Split vorhanden
  - `trust_return` ist als Helper gekapselt, aber nicht als neue Mechanik
    eingefÃ¼hrt
  - `decision_tendency` wertet `allow_plan=False` jetzt explizit vor `act`
    aus
  Umsetzung:
  - Abgleich in `docs/07_konstruktion/AKTUELLER_REGULATIONS_ABGLEICH.md`
    festgehalten
  - keine neue Handelsregel ergÃ¤nzt
  GeprÃ¼ft:
  - kompletter Testlauf erfolgreich

- [ ] EingangsgrÃ¶ÃŸen fÃ¼r `plan_allowed` prÃ¼fen.
  PrÃ¼fen:
  - `field_action_support`
  - `action_clearance`
  - `decision_strength`
  - `state_maturity`
  - `decision_readiness`
  - `review_feedback_state.act_push`
  - `temporal_conviction_boost`
  Ziel:
  - klÃ¤ren, ob `plan_allowed` durch echte innere TragfÃ¤higkeit entsteht oder
    durch zu starke Feedforward-/Review-/Temporal-VerstÃ¤rkung

- [x] `plan_allowed` an Meta-Regulator-Reflexion anbinden.
  Befund:
  - `plan_allowed` konnte bei hoher Denkhypothese handeln, obwohl die
    Meta-Regulation Ãœberkopplung, Impulsdruck oder geringe innere Distanz
    meldete
  Umsetzung:
  - `metaregulator_reflection_pressure` ergÃ¤nzt
  - Fallback-Handlung wird bei Ãœberkopplung weich zu `observe` oder `replan`
    zurÃ¼ckgefÃ¼hrt
  GeprÃ¼ft:
  - gezielter Regressionstest erfolgreich
  - kompletter Testlauf erfolgreich

- [x] Block V als Theorieanker dokumentieren.
  Befund:
  - Block V stÃ¼tzt die DIO-Architektur direkt: technische Logik bleibt
    Untergrund, Verhalten entsteht Ã¼ber Zustandsraum, Varianz,
    RÃ¼ckkopplung, Stabilisierung und emergente Musterbildung
  Umsetzung:
  - `docs/01_plan/UMSETZUNGSPLAN.md` ergÃ¤nzt
  - `README.md` ergÃ¤nzt
  - `docs/03_mechanik/WICHTIG_MECHANIKEN.md` ergÃ¤nzt
  Ziel:
  - klarstellen, dass die aktuelle Meta-Regulation keine harte Regel ist,
    sondern eine RÃ¼ckfÃ¼hrungsschicht gegen starre Impulsmotorik
- [x] Lauf 289: offene Hypothesen direkt an innere Handlungserlaubnis binden.
  Befund:
  - `confirmed_structural_interpretation` war im Lauf stark und profitabel
  - `open_structural_hypothesis` erzeugte die Haupt-Verlustlast
  - offene/reorganisierende Gedankenkeime durften zu oft motorisch handeln
  Umsetzung:
  - `thought_seed_state` wird im Entry-Gate gelesen
  - `seed_reinterpret` + schwache Erdung/Realitaetsbindung + offene
    Hypothesenspannung fuehrt weich zu `open_hypothesis_needs_replay`
  - bestaetigte/getragene Hypothesen bleiben handlungsfaehig
  Geprueft:
  - Gate-Regressionstests ergaenzt
  - kompletter Testlauf erfolgreich: `29/29`
  Weiter:
  - naechsten Debug auf Trade-Anzahl, `open_hypothesis_needs_replay`,
    `open_hypothesis_carried` und bestaetigte Strukturkontakte pruefen

- [x] Lauf 292: globalen Hypothesen-Trust auf passende Formfamilie begrenzen.
  Befund:
  - Lauf 292 war ruhiger, aber `open_structural_hypothesis` blieb komplett
    verlustreich
  - `dominant_hypothesis_trust_score` konnte eine aktuelle Hypothese stuetzen,
    auch wenn `dominant_hypothesis_trust_key` nicht zur aktuellen
    `form_symbol_id` gehoerte
  Umsetzung:
  - voller dominanter Trust wirkt nur bei passender Formfamilie
  - fremder dominanter Trust bleibt als schwacher Nachhall erhalten und erhoeht
    vorsichtig `borrowed_dominant_hypothesis_pressure`
  Geprueft:
  - kompletter Testlauf erfolgreich: `29/29`
  Weiter:
  - pruefen, ob offene Hypothesen weniger fremdes Vertrauen ausleihen und
    haeufiger in Replay/Observe gehen

- [x] Weltzeit/Denkzeit-Lag sichtbar machen.
  Befund:
  - nach Entkopplung von Backtest-Weltzeit und Denkzeit lief der Backtest sehr
    schnell, aber mit `0` Trades
  - bei `WORLD_TIME_SECONDS = 0.001` ist der volle kognitive Schritt deutlich
    langsamer als die Aussenwelt
  Umsetzung:
  - `GLOBAL_COGNITIVE_REACTION_SECONDS` auf `0.001` korrigiert
  - Bot-State um `world_published_ticks`, `world_missed_ticks`,
    `cognitive_lag_pressure` und `last_cognitive_lag_state` ergaenzt
  - `mcm_field_decision_protocol.csv` um Weltzeit-/Lag-Spalten erweitert
  Geprueft:
  - Compile-Check erfolgreich
  Weiter:
  - naechsten Lauf auf verpasste Weltfenster pruefen
  - danach schnelle Vorwahrnehmungs-/Kompressionsschicht bauen, damit DIO
    Weltbewegung verdichtet wahrnimmt, statt jeden Tick voll zu durchdenken

- [ ] Schnelle Vorwahrnehmung fuer Weltzeit/Denkzeit-Entkopplung bauen.
  Befund:
  - Lauf 360/361 zeigen trotz mehr Weltzeit weiter `0` Trades
  - mehr Weltzeit erhoeht die Anzahl verarbeiteter Runtime-Ticks deutlich,
    aber `cognitive_lag_pressure` bleibt hoch
  - DIO beobachtet/haelt mehr, aber die tiefe Kognition kommt weiterhin zu oft
    zu spaet oder zu schwer in Handlung naehe
  Ziel:
  - verpasste Weltbewegung als komprimierten Nachhall in den MCM-Raum geben
  - volle Denk-/Hypothesenschicht nur bei relevanten Formkontakten vertiefen
  - keine harte Handelsregel, sondern selektive Wahrnehmung und Lastregulation

- [x] Bewegte-Welt-Nachhall als erste Vorwahrnehmungsschicht umsetzen.
  Umsetzung:
  - `bot_engine/world_motion_afterimage.py` ergaenzt
  - verworfene Weltpakete bilden einen `world_motion_afterimage_state`
  - Nachhall wird in Runtime-Paket, Aussenweltzustand, Temporalitaet,
    Perception und Processing getragen
  - Feldentscheidungsprotokoll schreibt Nachhallstaerke, Druck, Richtung und
    Label
  Geprueft:
  - Compile-Check erfolgreich
  - Builder-Test erfolgreich
  Weiter:
  - naechsten Lauf auswerten: fuehrt bewegte Wahrnehmung zu weniger leerem
    Zurueckhalten und zu mehr qualitativen Kontakt-/Hypothesenmomenten?

- [x] Doppler-artige Nachhall-Achsen aus Bewegungsrestbild ableiten.
  Mechanik:
  - Aussenweltzeit, Innenzeit und Nachhall muessen getrennt bleiben
  - aus der Veraenderung des Nachhalls entsteht relative Bewegung:
    naeherkommend, abklingend, verdichtend, zerfallend
  Ziel:
  - moegliche Teilmuster und Fortsetzungsvarianten als Hinweisfeld bilden
  - keine Vorhersageregel, sondern MCM-konforme relative Wahrnehmung
  Moegliche Achsen:
  - `motion_approach_pressure`
  - `motion_recession_pressure`
  - `contact_frequency_shift`
  - `afterimage_doppler_bias`
  - `future_variant_pressure`
  Umsetzung:
  - Achsen in `bot_engine/world_motion_afterimage.py` abgeleitet
  - Werte in temporale Wahrnehmung, Perception, Processing und bewusste
    Wahrnehmung getragen
  - Debug-Protokoll um Doppler-/Vorhall-Spalten erweitert
  Geprueft:
  - Compile-Check erfolgreich
  - Builder-Test erfolgreich

- [ ] Doppler-/Vorhall-Achse im naechsten Lauf validieren.
  Pruefen:
  - erzeugt `future_variant_pressure` mehr gerichtete Beobachtung statt
    reaktiver Motorik?
  - steigt `afterimage_action_maturity` nur bei stabiler Restspur?
  - sinken act-Phasen unter `overcoupled_field`?
  - bleiben echte Trades an Formkontakt, MCM-Passung und innere Zustimmung
    gebunden?

- [x] Laeufe 363-365 nach Doppler-/Vorhall-Achse auswerten.
  Befund:
  - DIO uebertradet nicht; im 4-Monate-Lauf 365 nur `2` gefuellte Trades bei
    `4775` Attempts
  - alle gefuellten Trades liefen in SL, aber Drawdown blieb klein
  - `724` observed, `93` replanned, `3948` withheld
  - Beobachtungslernen ist aktiv: viele `saved_loss` und `missed_gain`
  - Hypothesenbestaetigung und Hypothesenablehnung liegen fast ausgeglichen
  - Hypothesen-Trust bleibt niedrig
  Deutung:
  - Doppler/Vorhall erzeugt keine wilde Motorik
  - Problem ist jetzt Hypothesenreifung: DIO sieht Moeglichkeiten, vertraut
    ihnen aber noch nicht tragfaehig genug
  Weiter:
  - Rueckfuehrung hypothetischer Beobachtung in Reife, Vertrauen und Vorsicht
    verstaerken
  - bestaetigte hypothetische Trades als Vertrauen speichern
  - verworfene oder belastende hypothetische Trades als Vorsicht und
    Reorganisation speichern

- [x] Rueckfuehrung hypothetischer Beobachtung in Familienreife verstaerken.
  Umsetzung:
  - beobachtete Hypothesen speichern zusaetzlich Compound, semantisches
    Formprofil, Hypothesenbestaetigung, Realitaetsbindung, strukturelle
    Erdung, Vorhall- und Nachhallreife
  - `saved_loss`/`missed_gain` wirken jetzt gewichtet auf exakte Form,
    Compound und semantisches Profil
  - Familien erhalten `trust_score`, `action_readiness` und `caution`
  - Review- und Entry-Gate koennen dominanten Hypothesen-Trust auch ueber
    passende Compound-/Semantikfamilie verwenden
  Geprueft:
  - Compile-Check erfolgreich
  - gezielter Hypothesen-Test erzeugt Trust in `fs`, `fc` und Profil
  Weiter:
  - naechsten Lauf auf `dominant_hypothesis_trust_key`,
    `dominant_hypothesis_action_readiness`, echte Trades und SL/TP-Verhalten
    pruefen

- [ ] Nachhall-Reife vor Handlungsnaehe einbauen.
  Befund aus Lauf 362:
  - Bewegte-Welt-Nachhall erzeugt wieder echte Handlung naehe
  - der einzige Trade lief aber in `sl_hit`
  - die Handlung entstand unter `overcoupled_field`, niedriger
    innerer/aeusserer Passung und schwacher Strategie-Bestaetigung
  Ziel:
  - Nachhall darf Wahrnehmung, Replay und Hypothesenpruefung aktivieren
  - Nachhall allein darf nicht als ausgereifte Handlungserlaubnis wirken
  - Handlung naeher ruecken, wenn Nachhall, Formkontakt, MCM-Gefuehl,
    Hypothesenbestaetigung und innere Zustimmung gemeinsam tragen
  Keine harte Sperre:
  - kein mechanisches Blockieren
  - eher eine Reifeschicht: bewegter Druck wird zuerst als Information
    verarbeitet, dann erst als moegliche Motorik

- [x] Lauf 366 nach Hypothesen-Familienrueckfuehrung auswerten.
  Befund:
  - `trades=0`, `submitted=0`, `filled=0`
  - Feldprotokoll zeigt aber `10` mal `act/plan_allowed`
  - `dominant_hypothesis_action_readiness` ist vorhanden
  - dominanter Trust-Key:
    `wide_form|wide_form_layer|quiet_form_family|single|named_form_packet`
  - `hypothesis_trust_family_count=80`
  Deutung:
  - Familienlernen funktioniert
  - Motorik ist nicht ueberaktiv, sondern zu stark gehemmt
  - kritischer Pfad ist jetzt:
    `act/plan_allowed` -> valider `MCM_ENTRY` -> Submission
  Zusatzfix:
  - KPI-Summary um `dominant_hypothesis_action_readiness`,
    `dominant_hypothesis_trust_evidence` und
    `hypothesis_trust_family_count` erweitert

- [ ] Planer-Bruecke zwischen Feldfreigabe und Entry pruefen.
  Problem:
  - Lauf 366 hatte `act/plan_allowed`, aber keine `entry_debug.csv`,
    keine `outcome_records.jsonl` und keine `trade_equity.csv`.
  - Das deutet darauf hin, dass der Tendenzpfad Handlung naeherlaesst, der
    konkrete Entry-Plan aber keinen gueltigen Trade liefert.
  Pruefen:
  - `build_runtime_decision_tendency`
  - `decide_mcm_brain_entry`
  - `derive_trade_plan_from_brain`
  - Uebergabe von `entry_mode`, `entry_choice_state`,
    `area_direct_readiness`, `strategic_entry_fit`
  - ob `plan_allowed` und konkreter Planer dieselbe innere Reife sehen
  Umsetzung Diagnose:
  - `entry_debug.csv` bekommt jetzt unsampled `MCM_ENTRY_BRIDGE`-Zeilen fuer
    `decision_plan_missing`, ungueltige Richtung, ungueltige Geometrie,
    abgelehnte innere Zustimmung und angenommene innere Handlung.
  - Damit kann der naechste Lauf die echte Bruchstelle zwischen MCM-Feld,
    Planer, innerer Zustimmung und Order-Pfad zeigen.
  Lauf 367:
  - 12 Monate 2025
  - `plan_allowed=263`
  - `inner_action_declined=238`
  - `inner_action_accepted=24`
  - `filled=11`
  - Netto ca. -2.51
  Befund:
  - kein fehlender Plan, keine ungueltige Entry-Geometrie
  - Problem ist akzeptierte Handlung bei schwacher Strategie-Tragfaehigkeit
  Umsetzung:
  - `strategy_contradiction_pressure` eingefuehrt
  - Strategie-Ablehnung staerker als Strategie-Bestaetigung wirkt jetzt als
    zusaetzliche innere Spannung auf `inner_no`
  - Wert wird in Entry-Debug und Trade-Stats sichtbar
  Lauf 368:
  - Trades auf 4 reduziert
  - Max DD kleiner, Nettoverlust kleiner, aber Handelsdichte fuer 12 Monate zu
    niedrig
  Nachjustierung:
  - `strategy_context_bearing` eingefuehrt
  - `raw_strategy_contradiction_pressure` bleibt als Rohwert sichtbar
  - wirksamer Widerspruchsdruck wird durch Kontext-Tragfaehigkeit moduliert
  - Einfluss auf `inner_no` von 0.75 auf 0.52 reduziert
  Lauf 369:
  - 4 Trades, 2 TP, 2 SL
  - Netto ca. +2.31
  - Max DD ca. 0.70 %
  - `plan_allowed` 360
  - `inner_action_accepted` 9
  - `inner_action_declined` 359
  Befund:
  - Feld sieht mehr Moeglichkeiten
  - innere Handlung bleibt selektiv
  - akzeptierte Motorik war in diesem Lauf tragfaehiger
  Naechster Schritt:
  - Rueckfuehrung zwischen abgelehnter Hypothese, spaeterem hypothetischem
    Ausgang und akzeptierter Handlung schaerfen
  Umsetzung:
  - Pending-Observations speichern Ablehnungsgrund, Consent-State und
    Strategie-/Widerspruchswerte mit.
  - aufgeloeste Beobachtungen werden nach Status, Ablehnungsgrund und
    Consent-State getrennt ausgewertet.
  - neue Summary-Werte:
    `declined_hypothesis_resolved`,
    `declined_hypothesis_saved_loss`,
    `declined_hypothesis_missed_gain`,
    `declined_hypothesis_confirmation_without_action`,
    `declined_hypothesis_rejection_without_action`,
    `declined_hypothesis_maturity`.
  - dadurch kann DIO spaeter unterscheiden, ob Nicht-Handeln Schutz war oder
    ob eine tragfaehige Hypothese verpasst wurde.
  Geprueft:
  - Compile sauber
  - isolierter Test fuer abgelehnte Hypothese mit spaeterem TP sauber
  Geprueft:
  - `py_compile` fuer `bot_gates/entry_decision.py` und `trading/trade_stats.py`
    sauber
- [ ] LONG-/SHORT- und Zustands-Wahrnehmungsspur im naechsten Lauf pruefen.
  Umsetzung:
  - `observation_outcome_by_side`
  - `observation_outcome_by_action_state`
  - `observation_outcome_by_side_rejection_reason`
  - `declined_long_hypothesis_*`
  - `declined_short_hypothesis_*`
  Ziel:
  - DIO soll LONG, SHORT, OBSERVE, REPLAN, WAIT/HOLD als eigene
    Handlungslagen mit eigener Konsequenzspur tragen.
  - Keine harte Bewertung der Richtung.
  - Richtung und Zustand werden als wahrgenommene Erfahrung gefuehrt.
  Pruefen:
  - ob LONG/SHORT getrennt befuellt werden.
  - ob LONG weiter belastet oder nur bestimmte LONG-Kontexte unreif sind.
  - ob SHORT weiterhin tragfaehiger wirkt.
  - ob Accepted/Declined stabil bleiben und kein Uebertrading entsteht.

- [ ] Richtungskontext fuer Hypothesen-Reifespur pruefen.
  Befund aus Lauf 372/373:
  - kein Uebertrading durch Reifespur-Rueckfuehrung.
  - Lauf 372: sehr vorsichtig, `2` Trades, ca. `+1.66`.
  - Lauf 373: etwas offener, `6` Trades, ca. `-0.68`.
  - Short trug Lauf 373, Long belastete.
  Naechster Fokus:
  - Reifespur nicht nur allgemein betrachten, sondern nach Seite und Kontext:
    Long-Hypothese, Short-Hypothese, Form/MCM-Familie, Kontaktreife,
    spaeterer hypothetischer Ausgang.

- [x] KPI-Spiegelung fuer `declined_hypothesis_*` korrigieren.
  Problem:
  - `observation_learning` enthielt die Werte korrekt.
  - `kpi_summary.observation_learning` zeigte weiter `0`.
  Ursache:
  - `_rebuild_kpi_summary()` uebernahm die Werte nicht in den internen
    `proof`-Block.
  Umsetzung:
  - `declined_hypothesis_*`,
    `dominant_hypothesis_action_readiness`,
    `dominant_hypothesis_trust_evidence` und
    `hypothesis_trust_family_count` werden jetzt in `proof` gespiegelt.
  Geprueft:
  - `python -m py_compile trading/trade_stats.py core/decision_regulation.py`
    sauber.

- [ ] Reifespur regulatorisch im naechsten Lauf pruefen.
  Umsetzung:
  - `declined_hypothesis_saved_loss` wirkt weich als Schutzspur:
    mehr Vorsicht, mehr Distanz, etwas mehr Motor-Spannung.
  - `declined_hypothesis_missed_gain` wirkt weich als verpasste
    Tragfaehigkeit:
    mehr Hypothesenvertrauen, mehr Bestaetigungsgewicht, etwas mehr
    Handlungserlaubnis.
  - gemischte Spuren wirken als Reorganisations-/Pruefspannung.
  - keine harte Freigabe, kein mechanisches Gate.
  Pruefen:
  - `inner_action_accepted`
  - `inner_action_declined`
  - `inner_state_needs_positive_confirmation`
  - `open_hypothesis_reality_check_need`
  - `open_hypothesis_action_permission`
  - Netto/Drawdown
  - ob `declined_hypothesis_*` jetzt auch im KPI-Block sichtbar ist.

- [x] Lauf 371 nach Kontextfix fuer abgelehnte Hypothesen pruefen.
  Ergebnis:
  - Equity ca. `106.2065`
  - Netto ca. `+6.2065`
  - Trades `9`, TP / SL `5 / 4`
  - Submitted / Filled `21 / 9`
  - Observed / Replanned / Withheld `4348 / 1243 / 9792`
  Befund:
  - Kontextfix greift.
  - `observation_outcome_by_rejection_reason` enthaelt echte Gruende.
  - `declined_hypothesis_resolved=15375`
  - `declined_hypothesis_saved_loss=8008`
  - `declined_hypothesis_missed_gain=7367`
  - `inner_state_declines_motor_action` war ueberwiegend schuetzend.
  - `inner_state_needs_positive_confirmation` ist ein moeglicher
    Uebergangsbereich fuer lernbares Vertrauen.
  Zusatzfix:
  - `trade_stats.json` baut `kpi_summary` vor dem Speichern erneut auf, damit
    die neuen `declined_hypothesis_*` Werte auch dort konsistent erscheinen.
  Geprueft:
  - `python -m py_compile trading/trade_stats.py` sauber.
  Naechster Schritt:
  - Reifespur regulatorisch rueckfuehren:
    schuetzende Ablehnung -> Vorsicht/Distanz;
    wiederholt verpasste tragfaehige Hypothese -> mehr Hypothesenvertrauen und
    gezieltere Realitaetspruefung, keine harte Freigabe.

- [x] Lauf 370 nach Reifespur fuer abgelehnte Hypothesen auswerten.
  Ergebnis:
  - Equity ca. `101.3860`
  - Netto ca. `+1.3860`
  - Trades `16`, TP / SL `7 / 9`
  - Submitted / Filled `24 / 16`
  - Max DD ca. `4.10 %`
  Befund:
  - DIO war aktiver als in Lauf 369.
  - Die neue Reifespur wurde zwar angelegt, aber die Kontext-Buckets blieben
    faktisch leer:
    `observation_outcome_by_rejection_reason` und
    `observation_outcome_by_consent_state` enthielten nur `-`.
  Ursache:
  - Refactor-Bruch in der Kontextuebergabe.
  - `build_entry_attempt_context()` und `TradeStats._compact_context()` waren
    nicht auf dieselbe Datenlage ausgerichtet.
  Umsetzung:
  - Entry-Kontext gibt Ablehnungsgrund, Consent-State, innere Zustimmung und
    Strategie-Werte jetzt auf Top-Level und in `trade_plan` aus.
  - TradeStats liest dieselben Werte robust aus Top-Level, `trade_plan`,
    `meta_regulation_state` und `action_intent_state`.
  - Hypothesis-Learning kann abgelehnte Hypothesen jetzt nach Status,
    Ablehnungsgrund und Consent-State auswerten.
  Geprueft:
  - `py_compile` sauber.
  - isolierter Kontexttest sauber.
  Naechster Pruefpunkt:
  - naechster Lauf muss echte Werte in
    `observation_outcome_by_rejection_reason`,
    `observation_outcome_by_consent_state` und `declined_hypothesis_*`
    zeigen.
# Offen: MCM-Possibility-Field im nÃ¤chsten Lauf prÃ¼fen

Status: offen

Nach dem Einbau von `core/possibility_field.py` muss der nÃ¤chste Lauf prÃ¼fen:

- Wird `mcm_possibility_field_state` sauber in `meta_regulation_state`
  geschrieben?
- Wechseln die ZustÃ¤nde sinnvoll zwischen:
  - `possibility_field_open`
  - `possibility_variant_cloud`
  - `possibility_observation_field`
  - `possibility_reflection_field`
  - `possibility_soft_collapse`
- Passt `possibility_dominant_direction` spÃ¤ter zur Konsequenz?
- Entsteht keine neue harte Handlungssperre?
- Entsteht kein erneutes Ãœbertrading durch `possibility_action_support`?

NÃ¤chster Schritt nach PrÃ¼fung:

BestÃ¤tigte Varianten sollen in Hypothesenreife und Vertrauen zurÃ¼ckgefÃ¼hrt
werden. Nicht tragende Varianten sollen Vorsicht, Abstand oder Reorganisation
stÃ¤rken. Das muss weich bleiben und darf kein starres Pattern-Gate werden.

- [x] Dokumentationsstruktur aufraeumen: `.md` aus `files/` nach `docs/`
  verschieben und nach Funktion kategorisieren.
  Ergebnis:
  - `files/` enthaelt nur noch `BILDER/`.
  - aktive Markdown-Dokumente liegen in `docs/00_regeln/`,
    `docs/01_plan/`, `docs/02_status/`, `docs/03_mechanik/`,
    `docs/04_berichte/`, `docs/05_gui/` und `docs/06_struktur/`.
  - `README.md`, `docs/README.md` und
    `docs/06_struktur/PROJEKTSTRUKTUR.md` sind auf die neue Struktur
    angepasst.

- [x] Root-Ordner `konstruktion/` in die Dokumentationsstruktur einordnen.
  Ergebnis:
  - Inhalt nach `docs/07_konstruktion/` verschoben.
  - `konstruktion/` als Root-Ordner entfernt.
  - Verweise in Markdown-Dateien aktualisiert.

- [x] Doppler-/Doppelspalt-Stand dokumentieren.
  Ergebnis:
  - Doppler-/Nachhall-Schicht als technisch umgesetzt eingeordnet.
  - MCM-Possibility-Field als erster Variantenraum eingeordnet.
  - Doppelspalt-Analogie als noch auszubauende Beobachter-/Reifemechanik
    festgehalten.
  - Umsetzungsplan, Mechanikdokument, Variablenmechanik und aktueller Stand
    ergaenzt.

- [x] Beobachter-/Reifemechanik fuer MCM-Possibility-Field umsetzen.
  Ziel:
  - offene Varianten ohne reale Order weiterbeobachten
  - spaeteren Realitaetskontakt auswerten
  - Bestaetigung, Ablehnung und Neutralitaet je Variantenfamilie speichern
  - Vertrauen, Vorsicht und Reorganisation weich in Meta-Regulation und
    Hypothesenlernen zurueckfuehren
  - kein starres Pattern-Gate und keine harte Handlungssperre erzeugen
  Umsetzung:
  - Possibility-Field erzeugt Beobachterzustand, Beobachtungstiefe,
    Realitaetskontakt, Variantenreife, Vertrauen und Vorsicht.
  - Pending Observations tragen diese Werte bis zur spaeteren Aufloesung.
  - `possibility_trust_families` speichert, welche Variantenfamilien sich
    tragend, belastend oder neutral gezeigt haben.
  - Review Feedback fuehrt dominante Moeglichkeitsfamilien weich in
    Handlungssupport oder Realitaetspruefung zurueck.
  Pruefung:
  - Compile der betroffenen Core-/Trading-Dateien OK.

- [ ] Naechsten Lauf auf Possibility-Observer-Reife pruefen.
  Fokus:
  - waechst `possibility_trust_families`
  - entstehen dominante Possibility-Varianten
  - steigen Vertrauen/Reife nur bei wiederkehrender Bestaetigung
  - steigt Vorsicht bei widerspruechlichem oder belastendem Realitaetskontakt
  - veraendert sich Tradeanzahl ohne hartes Gate

- [x] Innere Plan-Sperren aus nachgelagerter Regulation entfernen.
  Ergebnis:
  - `decision_regulation.py` verwendet Reorganisations-, Integrations-,
    Trust-Return- und Meta-Reflexionsdruck nicht mehr als harte
    `allow_plan=False`-Sperre.
  - `runtime_entry.py` verwendet Review-/Pattern-Druck nicht mehr als harte
    Plan-Sperre.
  - Die Gruende bleiben als `non_economic_plan_modulation_reasons` sichtbar.
  - Policy ist explizit `field_modulation_only`.

- [x] Nicht-Handeln sprachlich von Blockieren trennen.
  Ergebnis:
  - `entry_decision.py` gibt bei organischem Nicht-Handeln keine
    `execution_blocked=True`-Semantik mehr aus.
  - `inner_action_declined` wurde im Debug in `inner_action_reframed`
    umbenannt.

- [ ] Altbegriffe `signature_block` und `context_cluster_block` pruefen.
  Ziel:
  - Wenn diese Werte nur Diagnose sind, in `*_pressure`, `*_conflict` oder
    `*_modulation` umbenennen.
  - Wenn sie funktional noch als Sperre wirken, auf Feldmodulation
    zurueckbauen.

- [x] Harte Signatur-/Cluster-Erfahrungsbremse entfernen.
  Ergebnis:
  - `reinterpret_focus_by_signature()` setzt bei negativer Erinnerung nicht
    mehr direkt `decision = WAIT`.
  - Negative Signatur-/Cluster-Erfahrung erzeugt jetzt
    `*_caution_modulation`, `experience_caution_bias` und
    `memory_inhibition`.
  - `memory_effect = hard_inhibit` wurde entfernt und durch
    `caution_modulation` ersetzt.

- [x] Harte Attractor-/Stress-/Observation-Sperren im Fusionsentscheid
  entfernen.
  Ergebnis:
  - `defense_block` und `stressed_block` wurden zu Modulation.
  - `observation_mode` moduliert Score/Vorsicht, statt Long/Short hart zu
    deaktivieren.
  - `MCM_ATTRACTOR_LONG_ALLOW` und `MCM_ATTRACTOR_SHORT_ALLOW` wirken nicht
    mehr als hartes Gate, sondern als Score-Modulation.

- [ ] Laufvergleich nach Gate-Rueckbau.
  Pruefen:
  - Tradeanzahl gegen alte Referenz.
  - Anteil `observe/replan/hold/act`.
  - Auftreten von Mikrotrading.
  - PnL-Verlauf nicht als Hauptziel, sondern als Folge der organischen
    Entscheidungsqualitaet.

- [x] Offene Hypothesen von realer Entry-Naehe trennen.
  Anlass:
  - `debug_lauf_7` zeigte: bestaetigte Struktur war stark, offene/belastete
    Hypothesen wurden aber real gehandelt und liefen fast komplett in SL.
  Umsetzung:
  - `trading/trade_plan.py` fuehrt `hypothesis_reality_modulation` ein.
  - `confirmed_structural_interpretation` staerkt reale Entry-Naehe.
  - `open_structural_hypothesis`, belastete und reorganisierende
    Hypothesenspuren erhoehen Beobachtungsdruck und Motor-Restraint.
  - Kein hartes Gate: es wird nur die Reife/Nahe zur realen Order moduliert.

- [ ] Naechsten Lauf nach Hypothesen-Reality-Modulation pruefen.
  Fokus:
  - offene Hypothesen-Trades
  - bestaetigte Struktur-Trades
  - Long-/Short-Verteilung
  - `hypothesis_reality_state`
  - `hypothesis_observation_pressure`
  - `hypothesis_action_support`

