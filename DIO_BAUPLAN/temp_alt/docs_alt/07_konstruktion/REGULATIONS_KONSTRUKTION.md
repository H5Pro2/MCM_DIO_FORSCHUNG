# REGULATIONS-KONSTRUKTION

Herkunft der Extraktion:

`C:\Users\TV\Documents\24.05 v1 MCM_Trading_Brain`

Wichtig:
Der alte Code ist nur Herkunftsmaterial. Diese Datei ist die eigentliche
Referenz fuer den Wiederaufbau. Sie beschreibt die zu rekonstruierende
Verdrahtung, nicht den alten Monolithen als Kopiervorlage.

Relevante Dateien:

- `bot.py`
- `bot_gate_funktions.py`
- `MCM_Brain_Modell.py`
- `memory_state.py`
- `trade_stats.py`
- `config.py`

## 1. Grundprinzip der Konstruktion

Die zu rekonstruierende MCM-Regulation hat eine klare Reihenfolge:

1. Marktdaten werden als Runtime-Paket verarbeitet.
2. Das MCM-Brain bildet Wahrnehmung, Feldzustand, Denken und Meta-Regulation.
3. Daraus entsteht eine `decision_tendency`: `hold`, `observe`, `replan` oder `act`.
4. Das Gate laesst nur bei `decision_tendency == act` einen echten Entry-Plan zu.
5. Alles andere wird als Non-Action-Ereignis gespeichert: `withheld`, `observed_only` oder `replanned`.
6. Erst nach erfolgreichem Gate und Value-Gate entsteht Order-/Backtest-Ausfuehrung.
7. Ergebnis/Abbruch/Beobachtung fliesst als Outcome-Stimulus zurueck in MCM, Memory, Form-Sprache und Regulation.

Der entscheidende Schutz der Konstruktion:

`proposed_decision` war nur eine Hypothese. Handlung entstand erst, wenn die innere Regulation daraus `decision_tendency = act` machte.

## 2. Hauptfluss im Bot

Extrahierter Pfad aus dem alten Projekt:

```text
_process_market_packet_and_followup(packet)
  -> _process_market_packet(packet)
    -> _run_runtime_packet_action_cycle(resolved_packet)
      -> _advance_runtime_from_resolved_packet(resolved_packet)
        -> step_mcm_runtime(...)
          -> MCMBrainRuntime.advance(1)
            -> MCMBrainRuntime.tick()
              -> _compute_runtime_result(...)
              -> _apply_runtime_result(...)
      -> _run_runtime_action_cycle(window, candle_state)
        -> _run_runtime_execution_paths(...)
          -> _handle_active_position(...) oder _handle_entry_attempt(...)
```

Wichtig:

- Die Runtime wird zuerst aktualisiert.
- Danach entscheidet die Action-Schicht, ob offene Position, Pending Entry oder neuer Entry behandelt wird.
- Entry-Entscheidung nutzt nicht direkt Rohsignale, sondern den gespeicherten Runtime-Zustand.

## 3. Runtime-Objekt

Extrahierte Rolle:

`MCM_Brain_Modell.py`, `class MCMBrainRuntime`

Aufgabe:

- haelt letztes Marktpaket
- erkennt neuen Markttick ueber `_market_tick_pending`
- verwaltet `active_context_trace`
- ruft `_compute_runtime_result(...)`
- schreibt das Ergebnis ueber `_apply_runtime_result(...)` in den Bot

Wichtige Felder:

- `timestamp`
- `runtime_tick_seq`
- `last_impulse`
- `pending_impulse`
- `last_result`
- `brain_snapshot`
- `active_context_trace`
- `_market_tick_pending`

Wichtig fuer Rekonstruktion:

`tick()` darf nicht nur Signale berechnen. Es muss danach auch den Runtime-Zustand in den Bot schreiben:

- `bot.mcm_runtime_snapshot`
- `bot.mcm_runtime_decision_state`
- `bot.mcm_runtime_brain_snapshot`
- `bot.active_context_trace`
- `bot.felt_state`
- `bot.thought_state`
- `bot.temporal_perception_state`

## 4. Runtime-Ergebnis

Extrahierte Funktion:

`MCM_Brain_Modell.py`, `_compute_runtime_result(...)`

Rolle:

- entscheidet, ob bei aktiver Position/Pending Entry nur Hold/Observe gebaut wird
- ruft sonst `_compute_runtime_entry_result(...)`
- mappt das Entry-Result auf `decision_tendency`

Tendenz-Mapping-Kern:

```text
wenn active_position oder active_pending:
  runtime_hold_decision

sonst:
  runtime_entry_result berechnen
  wenn kein Result:
    runtime_hold_decision
  sonst:
    proposed_decision lesen
    meta_regulation_state lesen
    pre_action_phase lesen
    review_feedback + temporal_modulation lesen

    wenn proposed_decision LONG/SHORT:
      temporal/review pulls koennen observe/replan/hold erzwingen
      sonst act
    sonst:
      pre_action_phase / allow_observe / allow_ruminate bestimmen observe/replan/hold
```

Kritischer Punkt:

`proposed_decision` darf Richtung tragen, aber Non-Action-Zustaende laufen ueber `pre_action_phase`, `allow_observe`, `allow_ruminate`, Review-Feedback und Temporal-Modulation.

Fuer den aktuellen Wiederaufbau gilt:

- `allow_plan = False` darf nicht spaeter ueber `proposed_decision` wieder zu `act` werden.
- `proposed_decision` bleibt Hypothese, nicht Motorik.

## 5. Entry-State-Stack

Extrahierte Funktion:

`MCM_Brain_Modell.py`, `_compute_runtime_entry_result(...)`

Reihenfolge:

```text
1. tension_state = build_tension_state_from_window(window)
2. stimulus = build_mcm_stimulus(...)
3. snapshot = step_mcm_brain(...)
4. field_state = _derive_runtime_field_state(...)
5. update_target_model(...)
6. neural_state = build_neural_modulation(...)
7. fused_preview = resolve_fused_decision(...)
8. visual_market_state = build_visual_market_state(window)
9. structure_perception_state = STRUCTURE_ENGINE.build_structure_perception_state(window)
10. world_state = build_world_state(...)
11. outer_visual_perception_state = build_outer_visual_perception_state(world_state)
12. inner_field_perception_state = build_inner_field_perception_state(snapshot, bot)
13. perception_state = build_perception_state(world_state, bot)
14. processing_state = build_processing_state(...)
15. expectation_state = update_expectation_pressure_state(...)
16. felt_state = build_felt_state(...)
17. form_symbol_state = build_form_symbol_state(...)
18. state_signature = build_state_signature(...)
19. temporal_perception_state = build_temporal_coherence_state(...)
20. active_context_trace = _refresh_active_context_trace(...)
21. fused = reinterpret_focus_by_signature(...)
22. thought_state = build_thought_state(...)
23. meta_regulation_state = build_meta_regulation_state(...)
24. review_feedback_state = _resolve_review_decision_feedback(...)
25. strategic_window_state = build_strategic_window_state(...)
26. active_mcm_contact_state = build_active_mcm_contact_state(...)
27. bei allow_plan False: WAIT/Non-Action-Result
28. bei LONG/SHORT und Plan erlaubt: derive_trade_plan_from_brain(...)
```

Wichtige Kopplung:

- `felt_state`, `thought_state`, `form_symbol_state`, `temporal_perception_state`, `active_context_trace`, `strategic_window_state` und `active_mcm_contact_state` werden in `meta_regulation_state` integriert.
- Meta-Regulation entscheidet vor Trade-Plan.
- Trade-Plan ist nachgeordnet.

## 6. Meta-Regulation

Extrahierte Funktion:

`MCM_Brain_Modell.py`, `build_meta_regulation_state(...)`

Zentrale Eingaben:

- `perception_state`
- `processing_state`
- `felt_state`
- `thought_state`
- `fused`
- `pause_mode`
- `bot`

Zentrale Achsen:

- `uncertainty_score`
- `observe_priority`
- `signal_quality`
- `processing_load`
- `field_perception_pressure`
- `field_perception_support`
- `field_perception_clarity`
- `field_perception_fragmentation`
- `felt_pressure`
- `felt_conflict`
- `state_maturity`
- `decision_conflict`
- `decision_readiness`
- `long_hypothesis`
- `short_hypothesis`
- `decision_strength`
- `memory_support`
- `memory_inhibition`
- `memory_compare_load`
- `form_symbol_*`
- `structure_quality`
- `context_confidence`
- `route_familiarity`
- `transfer_bearing`
- `neurochemical_state`
- `conscious_perception_state`
- `temporal_*`

Kern fuer `decision_strength`:

```text
long_hypothesis = thought["long_hypothesis"]
short_hypothesis = thought["short_hypothesis"]
decision_strength = max(long_hypothesis, short_hypothesis)
```

Wichtig:

- kein `abs(long_score)`
- kein `abs(short_score)`
- Gegensignal darf nicht als Handlungsstaerke wirken
- `decision_strength` beschreibt tragende Hypothese, nicht rohen Druck

Pre-Action-Ausgabe:

- `allow_plan`
- `allow_observe`
- `allow_ruminate`
- `allow_block`
- `pre_action_phase`
- `rejection_reason`

Phasenlogik:

```text
pause / WAIT -> hold
observation_mode / Unsicherheit / Feldfragmentierung -> observe
Konflikt / Ueberlast / Replan-Druck -> replan
mangelnde Reife / zu wenig Readiness / Instabilitaet -> hold
klare Feldwahrnehmung und ausreichend Clearance -> act
sonst plan_allowed -> act
nachgelagerte Korrekturen koennen act wieder zu act_watch / observe / replan machen
```

Wichtig fuer Nachbau:

- Die erste Phase ist nicht endgueltig; nachgelagerte Schutzschichten koennen `allow_plan` wieder zuruecknehmen.
- `act_watch` ist kein echter Entry. Es ist gereifte Beobachtung unter Handlungsdruck.
- `zero_point_regulation` darf `allow_plan` in Beobachtung zurueckfuehren.
- Struktur-, Transfer-, visuelle und Formsymbol-Unsicherheit duerfen Handlung in Beobachtung/Replan umleiten.

## 7. Runtime-Tendenz als Gate-Schnittstelle

Extrahierte Funktion:

`MCM_Brain_Modell.py`, `build_runtime_decision_tendency(...)`

Rolle:

- liest `bot.mcm_runtime_decision_state`
- liest `bot.mcm_runtime_brain_snapshot`
- liefert eine kompakte Tendenz fuer das Gate
- baut bei Timestamp-Miss eine Hold-Decision

Wichtige Ausgabe:

- `decision_tendency`
- `proposed_decision`
- `allow_plan`
- `focus`
- `world_state`
- `structure_perception_state`
- `outer_visual_perception_state`
- `inner_field_perception_state`
- `perception_state`
- `processing_state`
- `felt_state`
- `thought_state`
- `meta_regulation_state`
- `expectation_state`
- `form_symbol_state`
- `strategic_window_state`
- `active_mcm_contact_state`
- Signatur-/Cluster-/Memory-/Feldwerte

Wichtig:

Das Gate bekommt keine frei schwebende Entscheidung, sondern einen bereits regulierten Runtime-Zustand.

## 8. Entry-Gate

Extrahierte Datei:

`bot_gate_funktions.py`

Extrahierte Funktion:

`evaluate_entry_decision(bot, window, candle_state)`

Verdrahtung:

```text
tendency_state = build_runtime_decision_tendency(...)

wenn tendency_state None:
  return None

decision_tendency = tendency_state["decision_tendency"]

wenn decision_tendency != "act":
  return Non-Action-Paket

sonst:
  decision = decide_mcm_brain_entry(...)
  pruefe side, entry, sl, tp, risk
  return Entry-Paket
```

Kritischer Schutz:

- Das Gate erzeugt keinen Brain-Plan, wenn die Runtime nicht `act` sagt.
- `observe`, `replan`, `hold`, `act_watch` bleiben Non-Action.
- `proposed_decision` bleibt als Hypothese im Kontext erhalten.

## 9. Non-Action-Verarbeitung im Bot

Extrahierte Funktion:

`bot.py`, `_handle_decision_tendency(entry_result)`

Mapping:

```text
decision_tendency == act      -> weiter zum Entry
decision_tendency == observe  -> event_name = observed_only
decision_tendency == replan   -> event_name = replanned
sonst                         -> event_name = withheld
```

Dann:

- Regulation Transition erfassen
- Attempt-Statistik schreiben
- Runtime Episode Event schreiben
- Regulation Snapshot committen
- kein Trade

Wichtig:

Non-Action ist kein Fehler und kein verpasster Trade. Es ist ein Lern-/Regulationsereignis.

## 10. Entry-Ausfuehrung nach Freigabe

Extrahierte Funktion:

`bot.py`, `_handle_entry_attempt(...)`

Reihenfolge:

1. keine Position / kein Pending Entry pruefen
2. externe Order pruefen
3. Pause abbauen
4. `evaluate_entry_decision(...)`
5. Non-Action ueber `_handle_decision_tendency(...)`
6. `value_gate.evaluate(entry_result)`
7. Geometrie pruefen: side, entry, tp, sl, risk
8. live/backtest Order vorbereiten
9. Outcome-/Attempt-Kontext speichern

Wichtig:

Value-Gate und Order-Geometrie liegen hinter der MCM-Regulation. Sie ersetzen nicht die Regulation.

## 11. Outcome-Rueckkopplung

Extrahierte Funktion:

`MCM_Brain_Modell.py`, `apply_outcome_stimulus(...)`

Rolle:

- Ergebnis/Abbruch/SL/TP/Cancel/Blocked wird in MCM-Feld, Form-Sprache, Erfahrung und neurochemische Diagnose zurueckgefuehrt.
- Outcome ist nicht nur Gewinn/Verlust, sondern Konsequenz fuer Wahrnehmung, Handlung, Gedanke und Kontakt.

Nachgelagerte Speicher-/Lernbereiche:

- `last_outcome_decomposition`
- `form_symbol_state`
- `mcm_decision_episode`
- `mcm_decision_episode_internal`
- `memory_state`
- `thought_state`
- `felt_state`
- `active_context_trace`

## 12. Rekonstruktionsregel

Wenn das aktuelle Projekt die MCM-Regulation wieder stabil nachbauen soll, muss folgende Kette erhalten bleiben:

```text
Wahrnehmung
-> Feld / MCM
-> Verarbeitung
-> Fühlen
-> Denken
-> Meta-Regulation
-> decision_tendency
-> Gate
-> nur bei act: Trade-Plan
-> Value-Gate / Order
-> Outcome-Stimulus
-> Memory / Feld / Form-Sprache
```

Nicht erlaubt als Refactor-Nebenwirkung:

- `proposed_decision` direkt handeln
- `allow_plan=False` spaeter wieder zu `act` machen
- Gegensignal ueber `abs(...)` als Staerke lesen
- Trade-Plan bauen, bevor Meta-Regulation die Handlung freigegeben hat
- Non-Action als Fehler oder leeren Pfad behandeln
- Runtime-State und Gate-State unterschiedlich interpretieren

## 13. Minimaler Verhaltensnachweis

Ein rekonstruiertes System muss in Debug/Stats wieder zeigen:

- `attempts_observed` sichtbar
- `attempts_replanned` sichtbar
- `attempts_withheld` sichtbar
- `attempts_skipped` oder gleichwertige Non-Action-Pfade sichtbar
- gefuellte Trades deutlich kleiner als Attempts
- `decision_tendency` nicht permanent `act`
- `pre_action_phase` nicht permanent `act`
- `allow_plan=False` fuehrt nicht zu Entry
- `act_watch` fuehrt nicht direkt zu Entry
