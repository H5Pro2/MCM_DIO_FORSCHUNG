# AKTUELLER REGULATIONS-ABGLEICH

Zweck:
Diese Datei gleicht die extrahierte Regulationskonstruktion gegen den aktuellen
Funktionssplit ab. Sie ist kein Wunschbild und keine Kopie des alten Codes,
sondern eine technische Prüfliste: Wo ist die Funktion heute, welcher
Datenvertrag muss gelten, welche Abweichung ist gefährlich.

## 1. Marktpaket -> Runtime

Konstruktionsrolle:

```text
Marktpaket
-> Runtime-Paket
-> MCM-Runtime aktualisieren
-> danach erst Action-Cycle
```

Aktueller Pfad:

```text
bot_engine/feed_runtime.py
  process_market_packet_and_followup

bot_engine/runtime_processing.py
  process_market_packet
  run_runtime_packet_action_cycle
  advance_runtime_from_resolved_packet

MCM_Brain_Modell.py
  step_mcm_runtime

core/runtime.py
  MCMBrainRuntime.advance
  MCMBrainRuntime.tick
```

Status:
Die Reihenfolge ist funktional richtig erhalten: Wahrnehmung und Runtime
werden vor dem Action-Cycle geschrieben. Das entspricht der Konstruktion.

Prüfpunkt:
`_runtime_seeded` und Timestamp-Synchronität müssen stabil bleiben. Wenn Gate
und Runtime unterschiedliche Timestamps lesen, muss der Pfad auf `hold`
zurückfallen, nicht auf Entry.

## 2. Runtime -> Entry-State-Stack

Konstruktionsrolle:

```text
tension
-> stimulus
-> MCM field / neural
-> fused hypothesis
-> visual / structure / world
-> perception / processing
-> felt
-> form language
-> temporal coherence
-> thought
-> meta regulation
-> review feedback
-> strategic window / active contact
```

Aktueller Pfad:

```text
MCM_Brain_Modell.py
  _compute_runtime_entry_result(...)

core/decision_regulation.py
  build_meta_regulation_state(...)
  _build_pre_action_decision_state(...)
```

Status:
Die Schichten sind im aktuellen Split vorhanden. Der wichtigste Schutz wurde
bereits wiederhergestellt: `decision_strength` wird aus tragenden Hypothesen
gebildet, nicht aus `abs(long_score/short_score)`.

Abgleich alt/aktuell:

- Alter funktioneller Pfad:
  `decision_strength = max(thought.long_hypothesis, thought.short_hypothesis)`
- Abweichung im aktuellen Split:
  zeitweise konnte zusätzlich `fused_state["decision_strength"]` einfließen.
- Korrektur:
  `decision_strength` kommt wieder nur aus den Denkhypothesen. Rohes oder
  vorverdichtetes Fused-Signal darf die Meta-Regulation nicht direkt
  übersteuern.

Prüfpunkt:
Alle neuen Schichten dürfen `allow_plan` zurücknehmen, aber nicht heimlich
wieder auf `True` setzen, wenn die Pre-Action-Schicht zuvor `observe`, `hold`
oder `replan` gebildet hat.

## 3. Meta-Regulation -> decision_tendency

Konstruktionsrolle:

```text
meta_regulation_state
  allow_plan
  pre_action_phase
  allow_observe
  allow_ruminate
  review_feedback
-> decision_tendency
```

Aktueller Pfad:

```text
MCM_Brain_Modell.py
  _compute_runtime_result(...)
```

Aktueller Schutz:

- Wenn `allow_plan == False`, wird nicht auf `act` gemappt.
- `pre_action_phase == replan` wird `replan`.
- `pre_action_phase == observe` oder `allow_observe` wird `observe`.
- sonst wird `hold`.

Das ist strenger als der alte Rohcode und fachlich korrekt, weil es die
Konstruktion schützt: innere Nicht-Freigabe darf nicht durch eine
LONG/SHORT-Hypothese überfahren werden.

Prüfpunkt:
`decision_tendency` darf nicht dauerhaft `act` werden. Wenn ein Lauf wieder
Mikrotrading zeigt, ist hier zuerst zu prüfen:

- wie oft `allow_plan=True` entsteht
- wie oft `pre_action_phase=act`
- ob `review_feedback_state.act_push` zu stark gegen Observe/Replan wirkt
- ob `temporal_conviction_boost` die Hemmung zu früh übersteuert

## 4. Runtime-State -> Gate

Konstruktionsrolle:

```text
build_runtime_decision_tendency
-> evaluate_entry_decision
-> nur bei decision_tendency == act: decide_mcm_brain_entry
```

Aktueller Pfad:

```text
core/runtime_tendency.py
  build_runtime_decision_tendency_view(...)

MCM_Brain_Modell.py
  build_runtime_decision_tendency(...)

bot_gates/entry_decision.py
  evaluate_entry_decision(...)
```

Status:
Der zentrale Gate-Schutz ist wieder vorhanden:

- `decision_tendency != act` gibt Non-Action zurück.
- `decision_tendency == act` mit `allow_plan=False` wird zu Non-Action.
- Erst danach wird `decide_mcm_brain_entry(...)` aufgerufen.

Erledigter Prüfpunkt:
Der aktuelle Gate-Pfad hatte noch einen Kompatibilitätspfad:

```text
if decision LONG/SHORT and no decision_tendency:
    behandle als act nach inner_action_consent
```

Dieser Pfad war für alte Schnittstellen gedacht, aber regulatorisch riskant,
wenn ein aktueller Runtime-State versehentlich ohne `decision_tendency`
ankommt. Er wurde für den DIO-Hauptpfad entfernt. Es gilt jetzt:

`decision_tendency` ist Pflichtfeld.

## 5. Non-Action-Verarbeitung

Konstruktionsrolle:

```text
observe -> observed_only
replan  -> replanned
sonst   -> withheld
```

Aktueller Pfad:

```text
bot_engine/execution_outcomes.py
  handle_decision_tendency(...)

bot_engine/entry_attempt.py
  handle_entry_attempt(...)
```

Status:
Die alte Rolle ist funktional erhalten. Non-Action wird als Attempt/Episode
gespeichert und führt nicht zum Value-Gate.

Prüfpunkt:
Wenn Debug wieder `withheld=0` oder `observed=0` zeigt, ist nicht zuerst die
Orderlogik schuld, sondern vorher die MCM-Entscheidungskette.

## 6. Entry-Ausführung

Konstruktionsrolle:

```text
MCM-Regulation erlaubt act
-> Entry-Plan lesen
-> Value-Gate
-> Geometrie prüfen
-> Order/Backtest
```

Aktueller Pfad:

```text
bot_engine/entry_attempt.py
  handle_entry_attempt(...)
```

Status:
Die Reihenfolge ist korrekt: Non-Action kommt vor Value-Gate und vor
Ordergeometrie.

Prüfpunkt:
Das Value-Gate darf keine MCM-Regulation ersetzen. Es ist nur nachgelagerter
Ausführungsschutz.

## 7. Funktionelle Zielmarken

Wir wollen nicht die alte PnL kopieren. Wir wollen das alte organische
Verhalten funktionell wieder erreichen:

- viele Wahrnehmungs-/Versuchsereignisse
- deutlich weniger echte Trades als Attempts
- sichtbare `withheld`, `observed_only`, `replanned`
- keine direkte Handlung aus `proposed_decision`
- keine Motorik aus Gegensignal-Betrag
- keine Entry-Plan-Erzeugung vor `decision_tendency=act`
- Outcome fließt in Feld, Memory, Formsprache und Episode zurück

## 8. Nächster technischer Abgleich

Als nächstes sind diese Stellen im aktuellen Code gegen die Konstruktion zu
prüfen:

1. Erzeugung von `allow_plan=True` in `core/decision_regulation.py`.
2. Verteilung von `pre_action_phase` im Debug.
3. `review_feedback_state`: Verhältnis `act_push`, `observe_pull`,
   `replan_pull`, `hold_pull`.
4. Debug-Stats: ob Non-Action wirklich als Attempt sichtbar bleibt.

## 9. Abgleich `allow_plan` und Trust-Return

Prüfung gegen den alten Funktionsstand:

- Die primären `allow_plan=True`-Auslöser sind im aktuellen Split funktional
  noch dieselben:
  - `field_perception_clear_act`
  - fallback `plan_allowed`
- Die nachgelagerten Rücknahmen sind ebenfalls vorhanden:
  - `act_watch`
  - `development_reframe_observe/replan`
  - `structure_orientation_observe`
  - `structure_development_observe`
  - `structure_bearing_observe`
  - `new_market_grammar_observe/replan`
  - `immature_transfer_observe/replan`
  - `transfer_break_observe/replan`
  - `pre_action_reorganization_observe/replan`
  - `diffuse_open_observe/reframe`
  - `integration_observe/reframe`
  - `cautious_hypothesis_observe/reframe`
  - `trust_return_stabilize_focus/replay`

Wichtige Abweichung zum alten Code:

- Der alte Code berechnete `trust_return` inline.
- Der aktuelle Split berechnet dieselbe Schicht über
  `_build_trust_return_state(...)`.

Bewertung:

Die Formeln und Eingangswerte wurden gegen den alten Stand geprüft. Der Helper
ist keine neue Mechanik, sondern eine Kapselung der alten Trust-Return-Schicht.
Wichtig bleibt: Der Helper muss mit `locals()` aus der Meta-Regulation gefüttert
werden, damit keine stillen Null-Defaults entstehen.

Zusätzlicher aktueller Schutz:

- Im aktuellen `build_runtime_decision_tendency(...)` wird `allow_plan=False`
  vor dem Mapping auf `act` ausgewertet.
- Das ist strenger als der alte Rohpfad, aber konstruktiv korrekt: Eine
  vorgeschlagene LONG/SHORT-Richtung darf die innere Nicht-Freigabe nicht
  überfahren.

Aktueller Debug-Hinweis:

- Der letzte vollständige Debug nach den Korrekturen zeigte wieder eine
  organischere Attempt-Verteilung: viele withheld-Ereignisse, deutlich weniger
  echte Trades.
- Das spricht dafür, dass die gröbste Motorik-Übersteuerung durch die letzten
  Gate-/Decision-Strength-Korrekturen entschärft wurde.

Nächster Prüfpunkt:

Nicht mehr zuerst die Orderlogik prüfen, sondern die Eingangsgrößen, die
`plan_allowed` überhaupt erreichen:

- `field_action_support`
- `action_clearance`
- `decision_strength`
- `state_maturity`
- `decision_readiness`
- `review_feedback_state.act_push`
- `temporal_conviction_boost`

## 10. Aktueller Debug-Snapshot nach Korrektur

Auswertung des letzten vollständigen Laufordners `debug_lauf_283`:

- Attempts: 800
- Gefüllte Trades: 26
- Withheld: 691
- Observed: 52
- Replanned: 1

`mcm_field_decision_protocol.csv`:

- `hold, decision_wait`: 168
- `hold, courage_hold`: 164
- `act, plan_allowed`: 39
- `observe, structure_development_observe`: 22
- `hold, pause_mode`: 21
- `observe, structure_bearing_observe`: 12
- weitere Observe/Replan-Ereignisse: niedrig

Interpretation:

Der fehlerhafte Zustand mit fast durchgehendem Mikrotrading ist im aktuellen
vollständigen Debug nicht mehr sichtbar. Die Motorik wird wieder überwiegend
durch Hold/Withheld gebremst. Trotzdem bleibt `plan_allowed` als Fallback der
nächste kritische Prüfpunkt, weil er dann greift, wenn keine feinere
Rücknahmebedingung vorher angesprochen hat.

## 11. Ergänzte Meta-Regulator-Rücknahme

Korrektur im aktuellen Split:

`plan_allowed` darf nicht nur deshalb zu Handlung werden, weil keine spezifische
Rücknahmebedingung gegriffen hat. Wenn der Meta-Regulator bereits Reflexion,
Überkopplung, Impulsdruck oder geringe innere Distanz meldet, muss diese
Innenlage mitsprechen.

Umsetzung:

- neue Diagnose-/Regulationsgröße:
  `metaregulator_reflection_pressure`
- Rücknahme nur bei:
  - `rejection_reason == plan_allowed`
  - LONG/SHORT liegt vor
  - Meta-Regulator meldet Reflexions-/Überkopplungszustand
  - Feldstütze, Innen-Außen-Abgleich oder Wahrnehmungsdistanz sind schwach
  - Handlungsclearance ist nicht eindeutig tragend

Wirkung:

Das ist keine harte Handelsregel. Es ist eine zusätzliche innere
Reflexionskopplung:

```text
Impuls kann Handlung vorbereiten.
Der Meta-Regulator darf aber sagen:
erst beobachten oder neu einordnen.
```

Damit bleibt DIO organisch: Handlung ist möglich, aber nicht gegen eine
gleichzeitig gemeldete innere Überkopplung.
