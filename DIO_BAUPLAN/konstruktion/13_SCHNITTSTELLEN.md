# 13 Schnittstellen

Diese Datei beschreibt die technische Übergabe zwischen den Schichten.

Ziel ist, dass DIO nicht als große vermischte Funktion gebaut wird, sondern als
klarer Wahrnehmungs- und Rückkopplungskreis.

## Laufzyklus

Pro Welt-Tick:

```text
world_state
-> visual_form_state
-> market_hearing_state
-> area_perception_profile
-> mcm_field_state
-> memory_match_state
-> thought_state
-> reality_check_state
-> action_state
-> consequence_state
-> regulation_state
```

## Welt

Ausgang `world_state`:

- `timestamp`
- `open`
- `high`
- `low`
- `close`
- `volume`
- `time_delta`
- `world_index`

`world_state` enthält keine fertige Deutung.

## Sehen

Ausgang `visual_form_state`:

- `form_id`
- `form_family`
- `direction_trace`
- `compression_trace`
- `area_trace`
- `recurrence_trace`
- `time_depth`
- `visual_uncertainty`

Ausgang `visual_sight_state`:

- `form_id`
- `form_family`
- `clarity`
- `object_stability`
- `coherence`
- `direction_bias`
- `range_position`
- `form_pressure`
- `form_resonance`
- `form_fragility`
- `depth`
- `contact_candidate`
- `background_load`
- `sight_label`

Diese Schnittstelle bleibt Sehen. Sie darf in Memory, Thought und
Aufmerksamkeit eingehen, aber nicht direkt als MCM-Feldlage oder Entry-Regel
verwendet werden.

Ausgang `visual_cortex_state`:

- `visual_cortex_label`
- `dominant_visual_object`
- `object_presence`
- `object_clarity`
- `relation_coherence`
- `visual_readiness`
- `trend_object_strength`
- `range_object_strength`
- `contact_object_strength`
- `compression_object_strength`
- `break_object_strength`
- `visual_object_relation_state`
- `visual_object_lifecycle_state`
- `visual_relation_label`
- `visual_lifecycle_label`
- `visual_object_side`
- `visual_object_distance`
- `visual_contact_nearness`
- `visual_object_binding_quality`
- `visual_cortex_grounding`

Diese Schnittstelle ist Chartlesen als Objektbildung. Sie beschreibt, welche
Art von visueller Struktur DIO erkennt. Sie bleibt vor Handlung und vor MCM-
Feldwirkung.

`visual_object_relation_state` beschreibt, wo ein Objekt im sichtbaren Raum
liegt und wie nahe es am Kontakt ist. `visual_object_lifecycle_state`
beschreibt, ob ein Objekt entsteht, stabil wird, Kontakt bekommt, abgewiesen
wird oder sich aufloest. Beides bleibt Seh-Kortex, nicht Entry-Logik.

`visual_cortex_grounding` ist die weiche Uebersetzung dieser Kortexqualitaet in
die Wahrnehmungsbilanz. Der Wert darf Sichtbindung staerken oder Pruefbedarf
anzeigen, aber keine Handlung freigeben.

Ausgang `market_hearing_state`:

- `loudness`
- `frequency_hz`
- `compression`
- `tone`

Sehen erzeugt Form und Hörwahrnehmung, keinen Trade.

## Multisensorische Bereichswahrnehmung

Ausgang `area_perception_profile`:

- `area_profile_id`
- `area_price_low`
- `area_price_high`
- `area_price_mid`
- `area_visual_profile`
- `area_hearing_profile`
- `area_temporal_profile`
- `area_mcm_contact_profile`
- `area_attention_need`
- `area_felt_depth`
- `area_multisensory_coherence`
- `area_overcoupling_risk`
- `area_profile_state`

Diese Schnittstelle ist als erste Wahrnehmungsschicht in
`core/area_perception.py` angelegt. Teile davon existieren weiterhin verteilt
in `strategic_window_state`, `area_contact_*`,
`sensory_area_coupling`, `felt_area_coupling` und
`thought_area_coupling`. Diese vorhandenen Felder liegen aber teilweise schon
nah an Entry, Kontakt oder Handlungsnaehe.

Der neue Bereichszustand muss davor liegen:

```text
visual_cortex_state
+ market_hearing_state
+ temporal_perception_state
+ gezielter MCM-Kontakt
-> area_perception_profile
```

`area_perception_profile` beschreibt, wie DIO einen Marktbereich erlebt:
sichtbar, hoerbar, zeitlich und bei Bedarf gefuehlt. Der Zustand darf
Aufmerksamkeit, Pruefbedarf und selektives Fuehlen anfordern. Er darf keine
Order, keine Richtung und keine Strategie erzwingen.

Aktuelle Anschlussstelle:

```text
area_perception_profile
-> build_active_mcm_contact_state
-> area_selective_contact_pull
-> area_selective_feel_permission
-> area_selective_feel_risk
```

Diese Werte sind Kontaktreize. Sie dürfen die Tiefe des MCM-Kontakts und die
Aufmerksamkeit modulieren, aber nicht selbst als Entry, Richtung oder
Handlungsfreigabe gelesen werden.

## Memory -> Kontaktnaehe

Ausgang `entry_contact_preference_memory`:

- `styles`
- `property_profiles`
- `selected_entry_preference_*`
- `selected_entry_property_profile_*`

Die Rueckfuehrung in den Trade-Plan erfolgt nicht als Gate, sondern als
organische Kontaktmodulation:

- `selected_memory_caution_pressure`
- `selected_memory_bearing_pressure`
- `mature_careful_contact_pressure`

`mature_careful_contact_pressure` bedeutet:

```text
Dieser Kontakt ist bekannt und gereift,
aber die gereifte Erfahrung ist vorsichtig oder belastet.
```

Wirkpfad:

```text
Memory-Eigenschaftsprofil
-> vorsichtige oder tragende Kontaktnaehe
-> receptive_contact_maturity
-> receptive_contact_immaturity_pressure
-> receptive_contact_restraint
-> area_contact_acceptance_pressure / area_contact_restraint_pressure
```

Das ist keine Handlungssperre. Es ist der Rueckweg erlebter Konsequenz in die
Koerpernaehe der naechsten Entscheidung.

## MCM-Feld

Ausgang `mcm_field_state`:

- `field_tension`
- `field_coherence`
- `field_bearing`
- `field_afterimage`
- `field_distance`
- `field_overcoupling`

Das MCM-Feld beschreibt innere Wirkung. Es ist kein Signalgeber.

Eingang in das MCM-Feld ist nicht die ganze Wahrnehmung, sondern nur die
reflektierte Wirkung ausgewaehlter Kontakte:

```text
visual_form_state       bleibt Sehen
market_hearing_state    bleibt Hoeren
thought_state           bleibt Thought

reflektive Wirkung:
-> tension
-> bearing
-> distance
-> overcoupling
-> afterimage
-> return_pressure
```

Verbotene Uebergabe:

```text
Formdaten direkt -> MCM-Feld
Frequenz direkt -> MCM-Feldrichtung
Hypothese direkt -> MCM-Realitaet
Entry-Wunsch direkt -> MCM-Tragfaehigkeit
```

Erlaubte Uebergabe:

```text
gesehener Kontakt -> gefuehlte Naehe / Distanz
gehoerte Energie -> neuronaler Stimulus / Nachhall
Gedanke -> Thought-Druck / Realitaetspruefungsbedarf
Konsequenz -> Entlastung / Belastung / Reorganisation
```

## Memory

Ausgang `memory_match_state`:

- `known_form_family`
- `similarity_trace`
- `past_bearing`
- `past_risk`
- `past_context`
- `memory_confidence`

Memory verweist auf reale Erfahrung, nicht auf freie Hypothese.

Schreibregel:

```text
memory_match_state darf nur reale Erfahrung referenzieren.
Gedankenbewertung gehört in Thought-Memory, nicht in Memory.
```

## Thought

Ausgang `thought_state`:

- `thought_id`
- `thought_family`
- `hypothesis_direction`
- `hypothesis_area`
- `hypothesis_reason`
- `thought_uncertainty`
- `thought_load`

Thought bildet Möglichkeiten. Thought ist keine Realität.

Schreibregel:

```text
thought_state braucht immer einen Realitätsanker:
reale Form + reale MCM-Wirkung + Zeitlage.
```

## Realitätsprüfung

Ausgang `reality_check_state`:

- `inner_outer_fit`
- `hypothesis_reality_fit`
- `form_mcm_fit`
- `maturity`
- `trust`
- `carefulness`
- `reorganization_pressure`

Die Realitätsprüfung übersetzt Gedanken in Reife, Vertrauen, Vorsicht oder
Reorganisation. Sie setzt keinen harten Block.

## Handlung

Ausgang `action_state`:

- `action_intention`
- `entry_area`
- `entry_price`
- `sl_price`
- `tp_price`
- `order_side`

Erweiterte Entry-Angebots-Schnittstelle:

- `entry_contact_options`
- `entry_contact_option_count`
- `entry_preference_state`
- `entry_choice_basis`
- `selected_entry_offer_score`
- `selected_entry_learned_fit`
- `selected_entry_preference_key`
- `selected_entry_preference_trust`
- `selected_entry_preference_caution`
- `selected_entry_preference_maturity`
- `selected_entry_preference_utility`
- `contact_learning_state`
- `learned_contact_fit`

Diese Felder beschreiben, welche Kontaktangebote DIO gesehen hat und warum ein
Angebot naeher lag. Sie duerfen nicht als starre Freigabe gelesen werden. Sie
zeigen nur die innere Praeferenzbildung aus Erfahrung, Bereich, Zeitlage und
MCM-Kontakt.
- `value_gate_passed`
- `action_distance`

Entry entsteht aus realer tragender Nähe. Hypothese darf deuten, aber nicht
allein handeln.

## Konsequenz

Ausgang `consequence_state`:

- `outcome_type`
- `realized_pnl`
- `trade_duration`
- `hypothesis_confirmed`
- `form_contact_confirmed`
- `mcm_contact_confirmed`
- `consequence_pressure`

Konsequenz wirkt zurück auf Feld, Memory, Thought und Regulation.

Entry-Kontaktpraeferenz:

- `entry_contact_learning`
- `entry_contact_preference_memory`
- `trust`
- `caution`
- `maturity`
- `utility`
- `property_profiles`
- `selected_entry_property_profile_*`

Diese Spur gehoert zur realen Konsequenz. Sie darf im naechsten Trade-Plan
weiche Naehe erzeugen, aber keine Handlung erzwingen.

Eigenschaftsprofile:

```text
reale Kontakt-Eigenschaften + reale Konsequenz
-> property_profiles
-> weicher Vergleich neuer Kontaktlagen
-> Vertrauen / Vorsicht / Reife / Nutzen modulieren
```

Diese Schnittstelle ist die Verallgemeinerung realer Erfahrung. Sie ersetzt
nicht die Realitaetspruefung und erzeugt keine vorprogrammierte Strategie.

Rückschreibregel:

```text
reale Konsequenz -> Memory
Gedanke bestätigt/widerlegt -> Thought-Memory
innere Wirkung -> MCM-Feld
Umgang damit -> Regulation
```

## Regulation

Ausgang `regulation_state`:

- `focus_level`
- `distance_level`
- `cognitive_load`
- `nervous_system_load`
- `action_depth`
- `reflection_pull`
- `recovery_need`

Regulation verändert die Haltung von DIO, nicht die Realität.
