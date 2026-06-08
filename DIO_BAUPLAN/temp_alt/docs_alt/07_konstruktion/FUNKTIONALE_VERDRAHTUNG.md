# FUNKTIONALE VERDRAHTUNG

Herkunft der Extraktion:

`C:\Users\TV\Documents\24.05 v1 MCM_Trading_Brain`

Diese Karte beschreibt die extrahierten Funktionsrollen und ihre heutige
Zielbedeutung. Der alte Code ist Quelle, nicht Ziel. Ziel ist die
rekonstruierte Verdrahtung im aktuellen Projekt.

## Bot-Layer

| Extrahierte Funktion | Alte Datei | Aufgabe | Muss im aktuellen Projekt entsprechen |
| --- | --- | --- | --- |
| `_process_market_packet_and_followup` | `bot.py` | Marktpacket verarbeiten und Follow-up/Flush ausloesen | `bot_engine/feed_runtime.py` |
| `_process_market_packet` | `bot.py` | Runtime-Paket bauen und Runtime-Zyklus starten | `bot_engine/runtime_processing.py` |
| `_run_runtime_packet_action_cycle` | `bot.py` | Runtime zuerst aktualisieren, danach Action-Cycle ausfuehren | `bot_engine/runtime_processing.py` |
| `_advance_runtime_from_resolved_packet` | `bot.py` | Marktpaket in MCM-Runtime einspeisen | `bot_engine/runtime_processing.py` |
| `_run_runtime_action_cycle` | `bot.py` | entscheidet zwischen Position, Pending Entry, neuer Entry | `bot_engine/action_context.py` |
| `_handle_entry_attempt` | `bot.py` | Gate, Non-Action, Value-Gate, Order-Vorbereitung | `bot_engine/entry_attempt.py` |
| `_handle_decision_tendency` | `bot.py` | `observe/replan/hold` als Non-Action speichern | `bot_engine/entry_attempt.py` oder eigener Non-Action-Helfer |

## Gate-Layer

| Extrahierte Funktion | Alte Datei | Aufgabe | Muss als Rolle erhalten bleiben |
| --- | --- | --- | --- |
| `evaluate_entry_decision` | `bot_gate_funktions.py` | Runtime-Tendenz lesen, nur bei `act` Brain-Plan holen | `bot_gates/entry_decision.py` |
| `build_runtime_decision_tendency` | `MCM_Brain_Modell.py` | gespeicherten Runtime-State fuer Gate verdichten | `core/runtime_tendency.py` |
| `decide_mcm_brain_entry` | `MCM_Brain_Modell.py` | bereits gespeicherten Entry-Plan aus Runtime-State lesen | `MCM_Brain_Modell.py` Bridge / `core/runtime_tendency.py` |

Wichtig:

`evaluate_entry_decision` darf nicht selbst aus Rohsignalen traden. Es liest Tendenz. Erst bei `act` liest es den Entry-Plan.

## Runtime-Layer

| Extrahierte Funktion/Klasse | Alte Datei | Aufgabe | Muss als Rolle erhalten bleiben |
| --- | --- | --- | --- |
| `MCMBrainRuntime` | `MCM_Brain_Modell.py` | Runtime-Gedaechtnis, Tick-Sequenz, aktiver Kontext | `core/runtime.py` |
| `step_mcm_runtime` | `MCM_Brain_Modell.py` | Bridge Runtime.advance | `core/runtime_bridge.py` |
| `_compute_runtime_result` | `MCM_Brain_Modell.py` | aktiver Trade/Pending oder Entry-State berechnen und Tendenz mappen | `core/runtime_entry.py` / Bridge |
| `_apply_runtime_result` | `MCM_Brain_Modell.py` | Ergebnis in Bot-Zustand schreiben | `core/runtime_entry.py` / Bridge |
| `_build_runtime_brain_snapshot` | `MCM_Brain_Modell.py` | aus Runtime-Result Snapshot fuer Gate/Debug bauen | `core/runtime_entry.py` |

Kritischer Datenvertrag:

- `mcm_runtime_snapshot`
- `mcm_runtime_decision_state`
- `mcm_runtime_brain_snapshot`
- `mcm_decision_episode`
- `mcm_decision_episode_internal`

Diese Objekte muessen konsistent bleiben.

## Entry-State-Stack

| Extrahierte Funktion | Alte Datei | Rolle |
| --- | --- | --- |
| `build_tension_state_from_window` | `MCM_Brain_Modell.py` | Chartenergie aus Fenster |
| `build_mcm_stimulus` | `MCM_Brain_Modell.py` | MCM-Reiz fuer Brain |
| `step_mcm_brain` | `MCM_Brain_Modell.py` | MCM-SNN/Feld tick |
| `_derive_runtime_field_state` | `MCM_Brain_Modell.py` | Feldzustand fuer Runtime |
| `build_neural_modulation` | `MCM_Brain_Modell.py` | neuronale Modulation/Neural State |
| `resolve_fused_decision` | `MCM_Brain_Modell.py` | vorlaeufige LONG/SHORT/WAIT-Hypothese |
| `build_visual_market_state` | `MCM_Brain_Modell.py` | visuelle Marktwahrnehmung |
| `STRUCTURE_ENGINE.build_structure_perception_state` | `MCM_Brain_Modell.py` | Strukturwahrnehmung |
| `build_world_state` | `MCM_Brain_Modell.py` | Aussenweltpaket |
| `build_outer_visual_perception_state` | `MCM_Brain_Modell.py` | aeussere Wahrnehmung |
| `build_inner_field_perception_state` | `MCM_Brain_Modell.py` | inneres MCM-Feld |
| `build_perception_state` | `MCM_Brain_Modell.py` | Wahrnehmungszusammenfassung |
| `build_processing_state` | `MCM_Brain_Modell.py` | Verarbeitungs-/Lastzustand |
| `update_expectation_pressure_state` | `MCM_Brain_Modell.py` | Erwartungsdruck |
| `build_felt_state` | `MCM_Brain_Modell.py` | innere Lage / Fuehlen |
| `build_form_symbol_state` | `MCM_Brain_Modell.py` | Formsprache / Symbolverdichtung |
| `build_state_signature` | `MCM_Brain_Modell.py` | Zustandssignatur |
| `build_temporal_coherence_state` | `MCM_Brain_Modell.py` | Zeit-/Raumzeit-Wahrnehmung |
| `_refresh_active_context_trace` | `MCM_Brain_Modell.py` | aktiver Kontext / Nachhall |
| `build_thought_state` | `MCM_Brain_Modell.py` | Hypothesen/Denken |
| `build_meta_regulation_state` | `MCM_Brain_Modell.py` | Freigabe, Beobachtung, Replan, Hold |
| `_resolve_review_decision_feedback` | `MCM_Brain_Modell.py` | Review/Memory Rueckmeldung |
| `build_strategic_window_state` | `MCM_Brain_Modell.py` | rueckblickender/raeumlicher Bereich |
| `build_active_mcm_contact_state` | `MCM_Brain_Modell.py` | aktiver Kontakt zwischen Aussen und Innen |
| `derive_trade_plan_from_brain` | `MCM_Brain_Modell.py` | Entry/SL/TP erst nach Regulation |

## Meta-Regulation: zentrale Ausgaben

Diese Felder muessen nach dem Split erhalten bleiben:

- `allow_plan`
- `allow_observe`
- `allow_ruminate`
- `allow_block`
- `pre_action_phase`
- `rejection_reason`
- `decision_strength`
- `decision_readiness`
- `state_maturity`
- `action_inhibition`
- `action_clearance`
- `regulated_courage`
- `field_observation_need`
- `field_replan_pressure`
- `field_action_support`
- `zero_point_regulation`
- `positive_zero_point_regulation`
- `structure_orientation_guard`
- `route_familiarity`
- `semantic_shift_pressure`
- `transfer_bearing`
- `interpretation_quality`
- `neurochemical_state`
- `conscious_perception_state`
- `active_mcm_contact_state`

## Nicht verwechseln

| Begriff | Bedeutung in der Konstruktion |
| --- | --- |
| `proposed_decision` | Hypothese/Richtung, noch keine Handlung |
| `decision_tendency` | regulierte Haltung: hold/observe/replan/act |
| `allow_plan` | Meta-Freigabe fuer Trade-Plan |
| `pre_action_phase` | innere Phase vor Handlung |
| `decision` im Entry-Result | erst bei erlaubtem Plan echte Richtung |
| `act_watch` | Beobachtung unter Handlungsdruck, kein direkter Trade |
| `withheld` | geregelte Nicht-Handlung, kein Fehler |
