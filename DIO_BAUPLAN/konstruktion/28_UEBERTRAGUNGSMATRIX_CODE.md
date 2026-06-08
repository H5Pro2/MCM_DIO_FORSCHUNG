# 28 Ãœbertragungsmatrix Code

Diese Datei mappt den bestehenden DIO-Code auf den aktiven Bauplan.

Ziel ist nicht, sofort alles umzubauen. Ziel ist eine klare Entscheidung:

```text
Welche Datei gehÃ¶rt zu welcher DIO-Schicht?
Was bleibt?
Was wird umbenannt oder vereinfacht?
Was wird spÃ¤ter entfernt?
```

Grundsatz:

```text
Der Ordnername `DIO_BAUPLAN` ist nur ein technischer Arbeitsort.
Fachlich ist dieser Inhalt der Bauplan und spÃ¤tere Konstruktionsplan fÃ¼r DIO.
Der bestehende Code wird daran zurÃ¼ckgefÃ¼hrt.
```

## Zielschichten

```text
Welt
-> Sinneswahrnehmung (Sehen + HÃ¶ren)
-> MCM-Feld
-> Memory
-> Thought
-> RealitÃ¤tsprÃ¼fung
-> Handlung
-> Konsequenz
-> Regulation
-> Debug / Visualisierung
```

## Kernwahrnehmung / Sensorische Trennung

FÃ¼r die weitere CodeprÃ¼fung gilt:

| Feld | DIO-Sinneskanal | Darf nicht direkt sein |
|---|---|---|
| `coherence` | FÃ¼hlen / MCM-Lage | fertige Handlung |
| `asymmetry` | Wahrnehmen / gerichtete PrÃ¤gung | Trade-Richtung als Regel |
| `energy` | HÃ¶ren / Frequenz, Kerzenspannung, Stimulus | direkte Feldlage oder Stressregel |

PrÃ¼fauftrag:

- `energy` darf stimulieren, aber nicht allein innere MCM-Lage, Stress,
  Chaos oder Entry erzeugen.
- `coherence` trÃ¤gt die gefÃ¼hlte Feldlage.
- `asymmetry` beschreibt PrÃ¤gung, nicht fertige Entscheidung.
- Alte `strategy_*`, `motor_*`, `action_*`-Felder sind auch darauf zu prÃ¼fen,
  ob sie diese drei SinneskanÃ¤le vermischen.

Erster Code-Stand:

| Datei | Ã„nderung |
|---|---|
| `bot_engine/mcm_core_engine.py` | ergÃ¤nzt `energy_raw_amplitude`, `energy_limited_amplitude`, `energy_amplitude_stimulus`, `energy_limiter_gain`, `energy_overdrive` und `energy_stimulus_channel` |
| `core/perception.py` | nutzt begrenzte LautstÃ¤rke statt direktem `energy - coherence`-Vergleich |
| `MCM_Brain_Modell.py` | alter Vision-Pfad fÃ¼hrt `auditory_stimulus`; hohe Energie wirkt nach Limiter weniger direkt als Bedrohung |

## Kernmatrix

| DIO-Schicht | Bestehende Datei(en) | Status | Entscheidung |
|---|---|---|---|
| Welt | `trading/csv_feed.py`, `trading/backtest_runtime.py`, `trading/live_runtime.py`, `bot_engine/market_packets.py`, `bot_engine/feed_runtime.py`, `bot_engine/runtime_timing.py` | grundsÃ¤tzlich passend | Behalten, aber Zeitbegriffe sauber trennen: Weltzeit, Backtest-Replay, Live-Polling, kognitives Budget. |
| Weltzustand / Paket | `bot_engine/runtime_processing.py`, `bot_engine/action_context.py`, `bot_engine/market_perception.py` | teilweise vermischt | Umbauen: Paketbildung darf nur Welt und aktuelle Wahrnehmung vorbereiten, keine fertige Handlung. |
| Sehen | `core/visual_perception.py`, `core/sensory_reality.py`, `core/perception.py`, `core/temporal_perception.py`, `bot_engine/visual_cortex_protocol.py`, `bot_engine/world_motion_afterimage.py` | wertvoll, aber breit | Behalten und vereinfachen: Ã¤uÃŸere Form, Bewegung, Zeit/Nachhall, Strukturkontakt. Keine Strategie in dieser Schicht. |
| Bereichswahrnehmung | `core/strategic_window.py` | fachlich nÃ¼tzlich, Name zu handlungsnah | Umbauen zu Bereichs-/RÃ¼ckblickwahrnehmung. Alte Felder bleiben Ãœbergang, neue Felder: `area_contact_pull`, `area_contact_timing_fit`, `area_future_present_coherence`. |
| MCM-Feld | `core/mcm_field.py`, `core/neurochemistry.py`, `core/felt_state.py`, `core/runtime_field_state.py`, `bot_engine/regulation_snapshot.py` | Kern bleibt | Behalten, aber Ãœberlappungen reduzieren. MCM-Feld ist innere GefÃ¼hlswahrnehmung, nicht Trading-Score. |
| MCM-Neuron / Modell | `core/mcm_model.py`, `core/brain_factory.py`, `core/runtime.py`, `core/runtime_bridge.py`, `MCM_Brain_Modell.py` | zu zentralisiert / Ãœbergang | Schrittweise weiter zerlegen. `MCM_Brain_Modell.py` bleibt vorerst Bridge, soll aber nicht wieder zum Monolith werden. |
| Formsprache | `core/form_language.py`, `core/form_symbol_orchestration.py`, `memory/form_symbol_memory.py` | wichtig | Behalten. DIOs eigene Syntax muss konsequent durch Memory, Thought und Debug laufen. |
| Memory real | `memory/memory_state.py`, `memory/form_symbol_memory.py`, `bot_memory/memory_state.json` | wichtig | Behalten. Nur reale Form/MCM/Konsequenz ankern. Keine Gedanken als RealitÃ¤t speichern. |
| Thought Memory | `core/thought_memory.py`, `memory/thought_memory_store.py`, `bot_memory/mcm_thought_memory.json` | wichtig, aber gefÃ¤hrlich | Behalten, aber strikt getrennt: Gedanken, Hypothesen, innere Syntax, keine absolute RealitÃ¤t. |
| Hypothesenlernen | `core/hypothesis_learning.py`, `core/review_feedback.py`, `core/possibility_field.py` | nÃ¼tzlich, aber handlungsnah | Umbauen: Hypothese = Denkspur. Bewertung Ã¼ber reale Konsequenz oder beobachtetes hypothetisches Ergebnis. Keine direkte Order-Motorik. |
| RealitÃ¤tsprÃ¼fung | `core/decision_regulation.py`, Teile von `core/runtime_entry.py`, Teile von `bot_gates/entry_decision.py` | zu groÃŸ / teils vermischt | Neu ordnen: Abgleich Form â†” MCM â†” Memory â†” Thought. Ergebnis ist NÃ¤he, Distanz, Reife, nicht sofort Entry. |
| Handlung / Entry | `trading/trade_plan.py`, `bot_gates/entry_decision.py`, `bot_engine/entry_attempt.py`, `bot_engine/pending_entry.py`, `bot_gates/trade_value_gate.py` | kritisch | ZurÃ¼ckfÃ¼hren: Handlung darf erst hinten entstehen. `trade_value_gate.py` bleibt einziges hartes Gate. `trade_plan.py` wird Handlungsadapter. |
| Order / Exchange | `trading/order_logic.py`, `trading/order_api_helpers.py`, `trading/exchange_data.py`, `api.py`, `workspace.py` | technisch getrennt genug | Behalten. Keine MCM-Logik hier einbauen. Nur AusfÃ¼hrung, Cancel, Status, Accountdaten. |
| Positionserleben | `bot_engine/active_position.py`, `bot_engine/exit_engine.py`, `bot_engine/matured_exit.py`, `bot_engine/exit_candidate_observe.py`, `bot_engine/position_intervention.py` | wichtig, aber spÃ¤ter | Behalten. SpÃ¤ter trennen: Positions-Erleben, Exit-Beobachtung, Intervention. Keine vorschnelle Exit-Intelligenz erzwingen. |
| Konsequenz | `bot_engine/execution_outcomes.py`, `core/runtime_commit.py`, `trading/trade_stats.py` | wichtig | Behalten. Konsequenz geht zurÃ¼ck in MCM-Feld, reales Memory und Thought Memory getrennt. |
| Debug / Protokolle | `debug_tools/writers.py`, `debug_tools/protocols.py`, `debug_tools/debug_reader.py`, `debug_tools/field_snapshots.py`, `trading/trade_stats.py` | Ã¼berladen | Aufteilen: GUI/KPI, Feldtopologie, Thought-Landkarte, Outcome, Runtime. Debug darf Architektur nicht steuern. |
| GUI | `_gui.py`, `_neuronen_gui.py`, `old_guis/` | nachrangig | SpÃ¤ter. GUI zeigt nur ausgewÃ¤hlte Organe und ZustÃ¤nde. Keine PrioritÃ¤t im Kernumbau. |
| Runner / Bot-Orchestrierung | `runner.py`, `bot.py`, `bot_engine/runtime_thread.py`, `bot_engine/runtime_followup.py`, `bot_engine/state_initialization.py` | notwendig | Behalten, aber Orchestrierung darf keine Fachlogik verstecken. |
| Konfiguration | `config.py` | zu groÃŸ | SpÃ¤ter bereinigen. Entfernen, was DIO selbst aus Erfahrung bestimmen soll. Harte technische Parameter bleiben. |

## Sofortige RÃ¼ckbau-Regeln

1. Keine neuen harten inneren Gates.
2. Nur das Value-Gate bleibt hart.
3. Hypothesen werden nicht als RealitÃ¤t behandelt.
4. Hypothesen erzeugen keine direkte Order.
5. Core erzeugt keine fertige Trading-Deutung.
6. Debug-Ausgaben dÃ¼rfen keine neue Denkstruktur erzwingen.
7. Alte Namen bleiben nur als Ãœbergang, wenn bestehende Protokolle sonst brechen.

## Begriffe, die zurÃ¼ckgefÃ¼hrt werden mÃ¼ssen

Diese Begriffe sind im bestehenden Code noch zu handlungsnah:

| Alter Begriff | Zielbegriff |
|---|---|
| `strategy_*` | `thought_*`, `contact_*`, `bearing_*` |
| `area_order_intention` | `area_contact_pull` |
| `area_action_timing_fit` | `area_contact_timing_fit` |
| `area_future_to_present_readiness` | `area_future_present_coherence` |
| `hypothesis_action_support` | `hypothesis_reality_bearing` oder `thought_confirmation_bearing` |
| `open_hypothesis_action_permission` | `open_hypothesis_reality_permission` |
| `dominant_hypothesis_action_readiness` | `dominant_hypothesis_reality_bearing` |
| `strategic_window` | Bereichs-/RÃ¼ckblickwahrnehmung |
| `trade_plan` | Handlungsadapter / Order-Geometrie |

## Zielverantwortung pro Schicht

### Welt

Welt liefert:

```text
Zeit
OHLCV
aktuelle Kerze
Replay-/Live-Kontext
```

Welt entscheidet nichts.

### Sehen

Sehen liefert:

```text
Form
Bewegung
Verdichtung
NÃ¤he
Nachhall
Zeit-/Raumtiefe
```

Sehen handelt nicht.

### MCM-Feld

MCM-Feld liefert:

```text
innere Wirkung
Spannung
TragfÃ¤higkeit
Druck
Entlastung
Ãœberkopplung
Zero-Point-RÃ¼ckfÃ¼hrung
```

MCM-Feld ist GefÃ¼hlswahrnehmung, kein Order-Generator.

### Memory

Memory liefert:

```text
reale Erfahrung
Formfamilien
MCM-Wirkung
Konsequenz
Wiederkehr
```

Memory speichert reale Kontakte, keine TagtrÃ¤ume als RealitÃ¤t.

### Thought

Thought liefert:

```text
Hypothese
gedachte Fortsetzung
innere Sprache
Deutung
Zweifel
BestÃ¤tigung
```

Thought bleibt eigene Gedankenschicht.

### RealitÃ¤tsprÃ¼fung

RealitÃ¤tsprÃ¼fung fragt:

```text
Passt mein Gedanke zur Form?
Passt mein MCM-GefÃ¼hl zur Form?
Kennt Memory reale Ã¤hnliche Kontakte?
Ist das tragende NÃ¤he oder nur innerer Druck?
```

Sie erzeugt Reife, Abstand oder HandlungsnÃ¤he.

### Handlung

Handlung entsteht nur, wenn vorher genug tragende NÃ¤he entsteht.

Handlung liefert:

```text
Entry-Kandidat
SL
TP
RR
Order-Geometrie
AusfÃ¼hrbarkeit
```

Das Value-Gate prÃ¼ft als einzige harte Sperre, ob das technisch/Ã¶konomisch
brauchbar ist.

### Konsequenz

Konsequenz liefert:

```text
TP
SL
Cancel
verpasste MÃ¶glichkeit
beobachtete Hypothese
Belastung
Entlastung
Reorganisation
```

Konsequenz verÃ¤ndert Feld, Memory und Thought getrennt.

## PrioritÃ¤t fÃ¼r den nÃ¤chsten Umbau

1. `trading/trade_plan.py` zu einem klaren Handlungsadapter zurÃ¼ckfÃ¼hren.
2. Hypothesenlogik aus Entry-Berechnung herausziehen.
3. `core/decision_regulation.py` in kleinere Rollen trennen:
   - Innenlage
   - RealitÃ¤tsprÃ¼fung
   - Reife
   - Vorsicht
   - HandlungsnÃ¤he
4. `core/strategic_window.py` spÃ¤ter umbenennen oder als Wahrnehmungsfenster
   neu einordnen.
5. Debug-Protokolle nach Zweck trennen.

## PrÃ¼fkriterium

Der bestehende DIO ist wieder auf Kurs, wenn gilt:

```text
Eine reale Form wird gesehen.
Das MCM-Feld spÃ¼rt eine Wirkung.
Memory erinnert reale Ã„hnlichkeit.
Thought bildet eine Hypothese.
RealitÃ¤tsprÃ¼fung prÃ¼ft diese Hypothese.
Handlung entsteht nur aus tragender NÃ¤he.
Konsequenz verÃ¤ndert Feld, Memory und Thought.
```

Wenn eine Hypothese direkt eine Order erzeugt, ist der Aufbau falsch.

## Umsetzungsschritt: Trade Plan als Handlungsadapter

`trading/trade_plan.py` wurde begonnen semantisch zurÃ¼ckzufÃ¼hren.

Ziel:

```text
Trade Plan = Order-Geometrie / Handlungsadapter
nicht Hypothesen-Kern
nicht Strategie-Zentrum
```

Neue Ãœbergangsfelder:

| Neues Feld | Bedeutung | Altes KompatibilitÃ¤tsfeld |
|---|---|---|
| `contact_entry_mode` | Art der realen Kontakt-Entry-NÃ¤he | `entry_mode` |
| `area_contact_weight` | Gewicht des Bereichskontakts | `strategic_entry_weight` |
| `area_contact_fit` | Passung des Bereichskontakts | `strategic_entry_fit` |
| `area_contact_intention` | Kontaktimpuls aus Bereichswahrnehmung | `area_motor_intention` |
| `impulse_perception_pressure` | Ã¤uÃŸerer Reizdruck, kein Entry-Anker | `impulse_entry_intention` |
| `area_order_geometry_intention` | Geometrische Entry-NÃ¤he aus Bereich | `area_entry_intention` |
| `entry_choice_pressure` | Konfliktdruck zwischen Reiz und Bereich | `entry_choice_conflict` |
| `entry_contact_bearing` | TragfÃ¤higkeit des Entry-Kontakts | `entry_choice_bearing` |
| `area_contact_readiness` | Reife des Bereichskontakts | `area_direct_readiness` |
| `area_contact_restraint` | ZurÃ¼ckhaltung des Bereichskontakts | `area_motor_restraint` |
| `entry_contact_state` | Zustand des Kontakts | `entry_choice_state` |
| `hypothesis_reality_bearing` | reale TragfÃ¤higkeit einer Hypothese | `hypothesis_action_support` |

Wichtig:

```text
Alte Felder bleiben vorerst bestehen.
Sie sind KompatibilitÃ¤t fÃ¼r Debug, Stats und vorhandene Schnittstellen.
Fachlich werden neue Felder bevorzugt.
```

Hypothesen werden im Trade Plan nicht als Entry-Anker gefÃ¼hrt. Sie kÃ¶nnen:

- Kontakt erklÃ¤ren
- Beobachtungsdruck erhÃ¶hen
- RealitÃ¤tsbindung anzeigen
- Reife oder Vorsicht modulieren

Sie dÃ¼rfen aber nicht allein eine Order erzeugen.

## Umsetzungsschritt: Nachgelagerte Pfade auf Kontaktfelder

Die nachgelagerten Pfade lesen jetzt bevorzugt die neuen Kontaktfelder:

- `core/runtime_entry.py`
- `bot_gates/entry_decision.py`
- `trading/trade_stats.py`

Wichtig:

```text
Neue Kontaktfelder haben Vorrang.
Alte motorische/strategische Felder bleiben Fallback.
```

Beispiele:

| Neuer Vorrang | Alter Fallback |
|---|---|
| `area_contact_intention` | `area_motor_intention` |
| `entry_contact_bearing` | `entry_choice_bearing` |
| `area_contact_readiness` | `area_direct_readiness` |
| `area_contact_restraint` | `area_motor_restraint` |
| `entry_contact_state` | `entry_choice_state` |
| `hypothesis_reality_bearing` | `hypothesis_action_support` |

Damit wird die laufende DIO-Version nÃ¤her an den Bauplan gefÃ¼hrt, ohne
bestehende Debug- oder Stats-Ausgaben sofort zu brechen.

## Umsetzungsschritt: Quellenfelder entkoppeln

Die ersten Quellenpfade geben jetzt ebenfalls DIO-konforme Namen aus.

| Neues Feld | Fachliche Bedeutung | Altes KompatibilitÃ¤tsfeld |
|---|---|---|
| `possibility_contact_bearing` | tragender Kontakt im Variantenraum | `possibility_action_support` |
| `open_hypothesis_reality_permission` | RealitÃ¤tsnÃ¤he einer offenen Hypothese | `open_hypothesis_action_permission` |
| `dominant_hypothesis_reality_bearing` | reale TragfÃ¤higkeit der dominanten Hypothese | `dominant_hypothesis_action_readiness` |

Wichtig:

```text
Diese Felder sind keine neuen harten Regeln.
Sie benennen die vorhandene Wirkung fachlich sauberer.
Alte Felder bleiben als technische Kopie, bis alle Ãœbergabepfade migriert sind.
```

ZusÃ¤tzlich wurde die irrefÃ¼hrende Restbezeichnung `impulse_preferred` im
Entry-Adapter durch `area_contact_weak` ersetzt. Wenn kein tragender
Bereichskontakt entsteht, entsteht weiterhin kein Entry.

Der Entry-Adapter arbeitet intern nun stÃ¤rker mit Kontaktbegriffen:

| Intern fÃ¼hrend | Alte Ausgabe nur als KompatibilitÃ¤t |
|---|---|
| `contact_entry_price` | `strategic_entry_price` |
| `contact_entry_weight` | `strategic_entry_weight` |
| `contact_entry_fit` | `strategic_entry_fit` |
| `area_contact_distance_fit` | `area_motor_distance_fit` |
| `entry_contact_pressure` | `entry_choice_pressure` / `entry_choice_conflict` |

Damit bleibt die technische AnschlussfÃ¤higkeit erhalten, wÃ¤hrend die fachliche
Interpretation vom Strategie-/Motorikbild weggefÃ¼hrt wird.

Die Ãœbergabepfade wurden nachgezogen:

- `core/runtime_entry.py`
- `bot_engine/entry_attempt_context.py`
- `bot_gates/entry_decision.py`
- `trading/trade_stats.py`

Sie lesen die neuen Kontaktfelder bevorzugt und schreiben alte Felder nur noch
als KompatibilitÃ¤t weiter.

NachprÃ¼fung:

- `bot_gates/entry_decision.py` muss im inneren Zustimmungswert `contact_fit`
  verwenden. `strategic_fit` ist dort kein fÃ¼hrender Wert mehr.
- Inferierte BeobachtungsplÃ¤ne aus `trading/trade_stats.py` mÃ¼ssen
  Kontaktfelder mitfÃ¼hren, damit spÃ¤tere Lern- und Debugspuren nicht wieder
  auf alte Strategie-/Motorikbegriffe zurÃ¼ckfallen.
- Der innere Zustimmungsregler bildet fachlich `thought_*`- und
  `contact_*`-Werte. `strategy_*` darf dort nur technische Kopie bleiben.

## Umsetzungsschritt: Reizdichte statt FeldÃ¼berlastung

`energy` wurde zuerst als Frequenz-/Stimuluskanal gefÃ¼hrt. Fachlich ist der
aktuelle Wert aber keine echte Frequenz, sondern KerzenlautstÃ¤rke /
Amplitude. Deshalb lÃ¤uft er jetzt zuerst durch einen sensorischen Limiter.

| Feld | Bedeutung |
|---|---|
| `energy_raw_amplitude` | rohe KerzenlautstÃ¤rke vor Sinnesfilter |
| `energy_limited_amplitude` | begrenzte wahrgenommene LautstÃ¤rke |
| `energy_amplitude_stimulus` | ReizstÃ¤rke, die in Wahrnehmung/Feld weitergeht |
| `energy_limiter_gain` | wie stark der Reiz gedÃ¤mpft wurde |
| `energy_overdrive` | Anteil, der zu laut war |
| `energy_frequency_stimulus` | alter Alias, fachlich nicht mehr fÃ¼hrend |

Ziel ist nicht, diese Einzelwerte Ã¼berall weiterzureichen. Sie sind technische
Zwischenwerte des Sinnesorgans. Nach auÃŸen soll daraus eine kompakte
HÃ¶r-Wahrnehmung entstehen:

```text
market_hearing_state
  loudness      = marktrelativ wahrgenommene LautstÃ¤rke
  frequency_hz  = Ãœbersetzung in einen einheitlichen HÃ¶rraum
  compression   = wie stark das Sinnesorgan dÃ¤mpfen musste
  tone          = DIOs eigene kurze Benennung dieser Marktmelodie
```

Damit kann jeder Markt seine eigene Melodie behalten, wÃ¤hrend DIO trotzdem
vergleichbare Wahrnehmung bekommt. BTC und SOL sollen nicht gleichgemacht
werden; sie sollen in einen gemeinsamen HÃ¶rraum Ã¼bersetzt werden.

Erster Code-Stand:

| Datei | Ã„nderung |
|---|---|
| `config.py` | fÃ¼hrt den Baseline-Zeitraum und den symbolischen HÃ¶rraum fÃ¼r `market_hearing_state` |
| `core/market_audio.py` | eigener Hoeradapter: Energie -> Lautstaerke/Frequenz/Kompression/Ton, ohne Handlungserlaubnis |
| `bot_engine/mcm_core_engine.py` | ruft den Hoeradapter auf und reicht `market_hearing_state` weiter |
| `core/perception.py` | reicht `market_hearing_state` in der Wahrnehmungsspur weiter |
| `MCM_Brain_Modell.py` | nutzt die marktrelative LautstÃ¤rke als `auditory_stimulus` |
| `core/runtime_entry.py` | reicht kompakte HÃ¶rwerte bis in das Entry-Result |
| `trading/trade_stats.py` | Ã¼bernimmt kompakte HÃ¶rwerte in Attempt-/Recent-Auswertung |

Die Frequenz ist bewusst noch kein Audio-Signal. Sie ist ein geordneter
Wahrnehmungswert: Wie hoch klingt die aktuelle Marktmelodie im VerhÃ¤ltnis zur
eigenen NormalitÃ¤t dieses Marktes?

Daraus folgt eine zweite Trennung im MCM-Feld:

| Neues Feld | Bedeutung | Darf nicht sein |
|---|---|---|
| `field_stimulus_density` | LautstÃ¤rke/AktivitÃ¤t des Ã¤uÃŸeren Reizraums | direkte Handlungsregel |
| `field_density` | innere Felddichte nach Verarbeitung | bloÃŸe Kopie von Energie |
| `regulatory_load` | tatsÃ¤chliche regulatorische Last | automatische Folge jeder hohen Energie |

Betroffene Dateien:

- `core/runtime_field_state.py`
- `core/runtime_entry.py`
- `core/runtime_snapshot.py`
- `MCM_Brain_Modell.py`
- `trading/trade_stats.py`

Damit kann ein spÃ¤terer Lauf zeigen, ob DIO wirklich Ã¼berlastet ist oder ob
der Markt nur stark stimuliert, ohne dass das innere Feld sofort kippt.
