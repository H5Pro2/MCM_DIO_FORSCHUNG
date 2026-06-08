# 29 Variablen und Wirkpfad

Diese Datei übernimmt die wichtigen Inhalte aus der alten
`MCM_VARIABLEN_MECHANIK.md` und `MCM_REZEPTOR_MATRIX.md` in die neue
DIO-Bauplan-Struktur.

Sie ist kein vollständiges Variablenlexikon. Sie ist die aktive Ordnung, nach
der Variablen künftig bewertet, behalten, umbenannt oder entfernt werden.

## Grundregel

Keine Variable ist eine Trading-Regel.

Zusaetzlich gilt fuer das MCM-Feld:

```text
Keine Sinnesvariable darf das Feld ersetzen.
Keine Thought-Variable darf als Realitaet ins Feld schreiben.
Keine Handlungsvariable darf Tragfaehigkeit vortaeuschen.
```

Das MCM-Feld bekommt nur reflektive Wirkungen. Rohdaten, Formdaten,
Hoerfrequenzen, Hypothesen und Entry-Absichten bleiben in ihrer eigenen
Schicht.

Der aktive technische Uebergang dafuer ist der Vorstufen-Regulator in
`core/mcm_preregulator.py`.

```text
Sehen/Hoeren/Memory/Thought/Outcome
-> Vorstufen-Regulator
-> mcm_reflective_*
-> MCM-Feld / Felt-State / Neurochemie
```

Damit wird verhindert, dass Formdaten, Frequenzen, Gedanken oder Outcome-Werte
als ungefilterte Realitaet in das MCM-Feld laufen.

Jede Variable muss in diesen Wirkpfad passen:

```text
Variable
-> Ebene
-> Rezeptorfamilie
-> Wirkung
-> Zielregler
-> Speicherpfad
-> Darf nicht
```

Wenn dieser Pfad nicht sauber angegeben werden kann, ist die Variable zu
unklar, doppelt oder gehört nicht in den Kern.

## Ebenen

| Ebene | Aufgabe |
|---|---|
| Welt | reale Außenwelt, Zeit, OHLCV, Bewegung |
| Sinneswahrnehmung | Form, Marktmelodie, sichtbare und hörbare Reize |
| MCM-Feld | gefühlte Wirkung, Spannung, Kohärenz, Nachhall |
| Memory | reale Erfahrung aus Form, Feld, Handlung/Nicht-Handlung und Konsequenz |
| Thought | Gedanken, Hypothesen, Varianten, innere Satzspuren |
| Realitätsprüfung | Abgleich zwischen Gedanke, Welt, Form, Feld und Memory |
| Handlung | reale Aktion oder bewusste Nicht-Handlung |
| Konsequenz | Rückwirkung der Realität |
| Regulation | Haltung, Abstand, Fokus, Reorganisation, Erholung |
| Neurochemie | Modulation von Feld, Neuronen und Regulation |

## Rezeptorfamilien

| Rezeptorfamilie | Frage | Beispiele |
|---|---|---|
| Außenreiz | Was kommt aus der Welt an? | `sensory_reality_pressure`, `visual_form_pressure`, `market_loudness` |
| Kontakt | Wie berühren sich Form und MCM-Feld? | `contact_overcoupling_risk`, `contact_temporal_bearing`, `contact_release_readiness` |
| Position | Wie wirkt eine offene reale Handlung? | `position_cognitive_load`, `position_mcm_field_strain`, `exit_decision_pressure` |
| Outcome | Was hat eine abgeschlossene Handlung oder Nicht-Handlung erzeugt? | `contact_utility_sample`, `contact_pain_sample`, `packet_process_reward` |
| Memory/Formsymbol | Was wurde persistent gelernt? | `form_symbol_contact_maturity`, `form_symbol_action_trust`, `form_symbol_caution_trust` |
| Thought | Wie wirkt ein Gedanke im inneren Feld? | `thought_load_pressure`, `open_hypothesis_replay_need`, `hypothesis_trust_score` |
| Neurochemie | Wie liest sich der innere Gesamtzustand? | `dopamine_tone`, `cortisol_load`, `gaba_inhibition`, `serotonin_stability` |
| Nachhall/Raumzeit | Was wirkt aus Vergangenheit, Bewegung oder Vorhall nach? | `subconscious_afterimage_pressure`, `world_motion_afterimage_strength`, `future_variant_pressure` |
| Sprache/Semantik | Woher kommt die Bezeichnung? | `dio_syntax_origin`, `self_foreign_boundary_clarity`, `semantic_origin_conflict` |

## Wirkarten

| Wirkart | Bedeutung | Speicher |
|---|---|---|
| Diagnose | macht Zustand sichtbar | nein oder nur Debug |
| weiche Regulation | verändert Haltung, Fokus, Nähe, Abstand | meist nein |
| Lernsample | einmaliger Abdruck aus Kontakt/Outcome | ja, aber verdichtet |
| persistente Erfahrung | wiederkehrende reale Erfahrung | ja |
| Thought-Spur | innere Hypothese oder Denkfamilie | ja, aber getrennt von Memory |
| Syntaxverdichtung | eigene DIO-Bezeichnung für Form/Feld/Gedanke | ja |

## Prüfregel gegen Doppelwirkung

Überlappung ist erlaubt, wenn Ebene, Zeitlage, Rezeptor oder Speicherstatus
unterschiedlich sind.

Kritisch ist eine Variable, wenn:

- sie dieselbe Bedeutung wie eine andere Variable trägt
- sie im selben Zeitfenster wirkt
- sie denselben Zielregler belastet
- kein anderer Rezeptor oder Speicherpfad sie trennt

Beispiel:

```text
field_overcoupling = gefühlte Überkopplung im MCM-Feld
distance_level     = regulatorischer Umgang mit dieser Überkopplung
```

Das ist erlaubt.

Nicht erlaubt wäre:

```text
zwei unabhängige Druckwerte erhöhen denselben Replan-Regler,
obwohl einer aus dem anderen berechnet wurde.
```

## Kernvariablen nach Schicht

### Sinneswahrnehmung

| Variable | Ebene | Rezeptor | Wirkung | Darf nicht |
|---|---|---|---|---|
| `visual_form_state` | Sehen | Außenreiz | sichtbare Form bündeln | Entry erzeugen |
| `visual_sight_state` | Sehen | Außenreiz | kompakten Sehzustand bündeln | MCM-Feld ersetzen |
| `visual_sight_state.form_family` | Sehen/Syntax | Außenreiz | gesehene Formfamilie verdichten | Strategie setzen |
| `visual_sight_state.contact_candidate` | Sehen | Außenreiz | möglichen visuellen Kontakt zeigen | Order auslösen |
| `visual_sight_state.background_load` | Sehen | Außenreiz | visuelles Hintergrundrauschen anzeigen | Feldstress direkt setzen |
| `visual_cortex_state` | Sehen/Kortex | Außenreiz | visuelle Objekte und Beziehungen bilden | Strategie ersetzen |
| `visual_cortex_state.dominant_visual_object` | Sehen/Kortex | Außenreiz | stärkstes visuelles Objekt benennen | Entry-Richtung setzen |
| `visual_cortex_state.visual_readiness` | Sehen/Kortex | Außenreiz | Lesbarkeit des visuellen Objekts zeigen | Handlungsfreigabe sein |
| `visual_object_relation_state` | Sehen/Kortex | Außenreiz | Lage, Kontaktnaehe und Objektbeziehung beschreiben | Entry-Anker sein |
| `visual_object_lifecycle_state` | Sehen/Kortex | Außenreiz | Entstehen, Stabilitaet, Kontakt, Zurueckweisung, Aufloesung beschreiben | Strategie erzwingen |
| `visual_relation_label` | Sehen/Syntax | Außenreiz | Beziehung des visuellen Objekts verdichten | Realitaetspruefung ersetzen |
| `visual_lifecycle_label` | Sehen/Syntax | Außenreiz | Lebenslauf des visuellen Objekts verdichten | Handlung freigeben |
| `visual_object_binding_quality` | Sehen/Kortex | Außenreiz | Objektbindung im Sehraum sichtbar machen | MCM-Tragfaehigkeit vortaeuschen |
| `visual_cortex_grounding` | Sehen/Regulation | Außenreiz | Kortex-Objektbindung in Seh-Erdung uebersetzen | Entry freigeben |
| `visual_clarity` | Sehen | Außenreiz | Formklarheit zeigen | Sicherheit erzwingen |
| `visual_object_stability` | Sehen | Außenreiz | Objektbindung sichtbar machen | Strategie setzen |
| `visual_form_novelty` | Sehen | Außenreiz | Neuheit zeigen | Alarm allein erzeugen |
| `visual_grounding_need` | Sehen/Regulation | Außenreiz | Bedarf nach Erdung | hart blockieren |
| `visual_attention_label` | Sehen | Außenreiz | Art der Betrachtung benennen | Handlung ausloesen |
| `visual_form_contact` | Sehen | Außenreiz/Kontakt | sichtbaren Formkontakt zeigen | MCM-Feld ersetzen |
| `visual_inspection_pull` | Sehen/Regulation | Außenreiz | Zug zum genaueren Betrachten | Dauerdruck erzeugen |
| `visual_attention_depth` | Sehen | Außenreiz | Betrachtungstiefe zeigen | Sicherheit erzwingen |
| `visual_background_filter` | Sehen/Regulation | Außenreiz | Hintergrundreiz daempfen | Information loeschen |
| `visual_mcm_contact_weight` | Sehen->MCM | Kontakt | Weitergabegewicht ins Feld | Entry-Anker sein |
| `visual_impulse` | Sehen/MCM-Neuron | Sensorik | neuronale Sehspur sichtbar machen | Entry-Impuls sein |
| `visual_afterimage` | Sehen/MCM-Neuron | Nachbild | visuelle Restform im neuronalen Feld tragen | Zukunft beweisen |
| `visual_resonance` | Sehen/MCM-Neuron | Resonanz | Reaktion des Neurons auf sichtbare Form zeigen | Handlungserlaubnis sein |
| `visual_neural_action_permission` | Sehen/Motorik-Trennung | Schutzwert | muss aktuell `0.0` bleiben | Trade freigeben |
| `market_hearing_state` | Hören | Außenreiz | Marktmelodie bündeln | Feldstress direkt setzen |
| `market_loudness` | Hören | Außenreiz | relative Lautstärke | als Chaosregel wirken |
| `frequency_hz` | Hören | Außenreiz | Energie in Hörraum übersetzen | Richtung vorgeben |
| `auditory_impulse` | Hoeren/MCM-Neuron | Sensorik | neuronale Hoerspur sichtbar machen | Entry-Impuls sein |
| `auditory_aftertone` | Hoeren/MCM-Neuron | Nachhall | Restklang im neuronalen Feld tragen | Marktvorhersage sein |
| `auditory_resonance` | Hoeren/MCM-Neuron | Resonanz | Reaktion des Neurons auf Marktklang zeigen | Handlungserlaubnis sein |
| `auditory_neural_action_permission` | Hoeren/Motorik-Trennung | Schutzwert | muss aktuell `0.0` bleiben | Trade freigeben |

### Multisensorische Bereichswahrnehmung

Diese Schicht ist als erste Code-Fassung in `core/area_perception.py`
angelegt. Sie ersetzt nicht Sehen, Hoeren oder MCM-Feld, sondern buendelt
einen konkreten Marktbereich als erlebbaren Wahrnehmungsraum.

| Variable | Ebene | Rezeptor | Wirkung | Darf nicht |
|---|---|---|---|---|
| `area_perception_profile` | Bereichswahrnehmung | multisensorisch | sichtbare, hoerbare, zeitliche und gefuehlte Bereichslage buendeln | Entry-Signal sein |
| `area_visual_profile` | Sehen/Bereich | Aussenreiz | Form, Objektbeziehung und Kontaktnaehe eines Bereichs beschreiben | MCM-Feld ersetzen |
| `area_hearing_profile` | Hoeren/Bereich | Aussenreiz | Lautheit, Frequenz und Kompression eines Bereichs beschreiben | Richtung setzen |
| `area_temporal_profile` | Raumzeit/Bereich | Nachhall | Zeitlage, Nachhall und Bewegungsbezug eines Bereichs tragen | Zukunft beweisen |
| `area_mcm_contact_profile` | MCM-Kontakt | Kontakt | gezielte Feldwirkung eines Bereichs beschreiben | Rohform speichern |
| `area_attention_need` | Regulation/Bereich | Aufmerksamkeit | Bedarf nach genauerem Sehen/Hoeren/Fuehlen anzeigen | Dauerdruck erzeugen |
| `area_felt_depth` | MCM-Kontakt | Kontaktintensitaet | zeigen, wie tief DIO diesen Bereich fuehlt | Handlung erzwingen |
| `area_multisensory_coherence` | Realitaetspruefung/Bereich | Kopplung | Passung zwischen Sehen, Hoeren, Zeit und Fuehlen zeigen | Value-Gate ersetzen |
| `area_overcoupling_risk` | Regulation/Bereich | Schutz | Ueberkopplung durch zu starkes Bereichsfuehlen anzeigen | Bereich loeschen |
| `area_profile_state` | Sprache/Bereich | Semantik | DIOs kurze Benennung des Bereichserlebens tragen | absolute Wahrheit sein |
| `area_selective_contact_pull` | MCM-Kontakt/Bereich | Kontaktreiz | sichtbaren/hoerbaren Bereich in gezieltes Fühlen ziehen | Entry auslösen |
| `area_selective_feel_permission` | MCM-Kontakt/Bereich | Kontakt-Erlaubnis | selektive Fühl-Tiefe unterstützen, wenn Bereich kohärent genug wirkt | Gate sein |
| `area_selective_feel_risk` | MCM-Kontakt/Bereich | Schutz | Überkopplung anzeigen, wenn Bereich mehr zieht als trägt | Bereich blockieren |

### MCM-Feld

| Variable | Ebene | Rezeptor | Wirkung | Darf nicht |
|---|---|---|---|---|
| `field_tension` | MCM-Feld | Kontakt | Feldspannung zeigen | Entscheidung sein |
| `field_coherence` | MCM-Feld | Kontakt | Stimmigkeit der Feldlage | Entry freigeben |
| `field_bearing` | MCM-Feld | Kontakt | gefühlte Tragfähigkeit | Profitlabel sein |
| `field_afterimage` | MCM-Feld/Raumzeit | Nachhall | Restwirkung tragen | Realität ersetzen |
| `field_distance` | MCM-Feld | Kontakt | gefühlte Distanz | Regulation ersetzen |
| `field_overcoupling` | MCM-Feld | Kontakt | zu starke Kopplung zeigen | harte Sperre sein |
| `field_bearing_support` | MCM-Feld | Kontakt | Feldtragfaehigkeit fuer Regulation lesbar machen | Handlungsbefehl sein |
| `action_readiness_from_field` | Regulation | Kontaktuebersetzung | Feldtragfaehigkeit in Handlungsnaehe uebersetzen | MCM-Feld ersetzen |
| `field_action_support` | Kompatibilitaet | Alt-Alias | alter Uebergangsname fuer bestehende Pfade | neue Fachlogik sein |
| `mcm_reflective_bearing` | Vorstufe->MCM | Normierung | tragende Wirkung aus Sehen, Hoeren, Memory, Thought und Outcome buendeln | Profitlabel sein |
| `mcm_reflective_pressure` | Vorstufe->MCM | Normierung | belastende Wirkung vor dem Feld buendeln | Rohstress doppeln |
| `mcm_reflective_coupling_load` | Vorstufe->MCM | Kontaktlast | zeigen, wie stark Quellen ans Feld koppeln | Handlungsfreigabe sein |
| `mcm_reflective_displacement` | Vorstufe->MCM | Auslenkung | normierte Feldrichtung -1..+1 vor MCM-Skalierung | Rohkohaerenz sein |
| `mcm_reflective_field_position` | Vorstufe->MCM | Feldlage | normierte Lage -3..+3 aus Vorstufenwirkung | echte Feldhistorie ersetzen |
| `mcm_reflective_tension` | Vorstufe->MCM | Spannung | Gesamtspannung aus Druck, Kopplung und Auslenkung | Trade-Druck sein |
| `mcm_preregulator_state` | Vorstufe | Matrix | Kanaele und Gesamtwirkung dokumentieren | Debug-Muell werden |

Reflektive Grenze:

```text
MCM-Feldwerte duerfen nur Wirkung ausdruecken:
Spannung, Auslenkung, Naehe, Distanz, Tragfaehigkeit, Nachhall.

MCM-Feldwerte duerfen keine Rohform, keinen Patternnamen, keine Frequenz,
keine Hypothese und keine Orderabsicht enthalten.
```

Wenn ein Wert zugleich Formbeschreibung und Feldwirkung ist, muss er getrennt
werden:

```text
visual_form_contact        = ich sehe einen Kontakt
visual_mcm_contact_weight  = wie stark dieser Kontakt ans Feld weitergegeben wird
field_bearing              = wie tragend der Kontakt im Feld wirkt
```

Wenn ein Wert zugleich Feld und Handlung benennt, muss er ebenfalls getrennt
werden:

```text
field_bearing_support      = Feld traegt Kontakt
action_readiness_from_field = Regulation uebersetzt Feld in Handlungsnaehe
field_action_support       = nur noch alter Alias waehrend des Rueckbaus
```

### Thought und Denkökonomie

| Variable | Ebene | Rezeptor | Wirkung | Darf nicht |
|---|---|---|---|---|
| `perception_event_strength` | Thought/Sehen | Außenreiz | Denken an echten Kontakt binden | Dauerdruck erzeugen |
| `thought_load_pressure` | Thought | Thought | Denklast sichtbar machen | Denken verbieten |
| `thought_overprocessing_signal` | Thought/Regulation | Thought | Überdenken anzeigen | hart stoppen |
| `thought_economy_need` | Regulation | Thought | sparsameres Denken anfordern | Hypothese löschen |
| `thought_release_pressure` | Thought/Regulation | Thought | Loslassen/Reframing nahelegen | Information verwerfen |
| `thought_efficiency_support` | Thought | Thought | getragenes Denken zeigen | Handlung erzwingen |

### MCM-Spannungsachse

Skalentrennung:

- `mcm_axis_displacement` ist ein normalisierter Rechenwert im Bereich
  `-1 .. +1`.
- `mcm_axis_field_position` ist die fachliche MCM-Feldposition im Bereich
  `-3 .. 0 .. +3`.

| Variable | Ebene | Rezeptor | Wirkung | Darf nicht |
|---|---|---|---|---|
| `mcm_axis_displacement` | MCM-Feld | Kontakt/Neurochemie | normalisierte Richtung der Auslenkung | als volle Feldlage gelesen werden |
| `mcm_axis_field_position` | MCM-Feld | Kontakt/Neurochemie | Feldposition im Bereich `-3 .. +3` | gut/schlecht setzen |
| `mcm_axis_tension` | MCM-Feld | Kontakt/Neurochemie | Stärke der Auslenkung | Trade-Nähe erzwingen |
| `mcm_axis_state` | Sprache/MCM | Semantik | `--`, `-`, `0`, `+`, `++` verdichten | absolute Wahrheit sein |
| `positive_expansion_pressure` | Neurochemie/MCM | Neurochemie | expansive Spannung zeigen | Belohnungssignal allein sein |
| `negative_contraction_pressure` | Neurochemie/MCM | Neurochemie | kontraktive Spannung zeigen | Verlustsignal allein sein |

### Handlung / Entry-Angebote

| Variable | Ebene | Rezeptor | Wirkung | Darf nicht |
|---|---|---|---|---|
| `entry_contact_options` | Handlungsvorstufe | Kontaktangebote | mehrere mögliche Bereichskontakte sichtbar machen | fertige Strategie sein |
| `entry_contact_option_count` | Handlungsvorstufe | Übersicht | Anzahl der angebotenen Kontakte tragen | Qualitätswert sein |
| `entry_preference_state` | Handlung/Kontakt | Präferenz | zeigen, ob DIO eine eigene Kontaktpräferenz bildet | hartes Gate sein |
| `entry_choice_basis` | Handlung/Kontakt | Begründung | Herkunft der Auswahl benennen | Regel erzwingen |
| `selected_entry_offer_score` | Handlung/Kontakt | Verdichtung | aktuell gewählte Kontakt-Nähe beschreiben | alleine handeln |
| `selected_entry_learned_fit` | Memory/Handlung | Erfahrung | gelernte Tragfähigkeit der gewählten Kontaktart einbringen | Zukunft beweisen |
| `learned_contact_fit` | Memory/MCM | Erfahrung | Kontaktreife, Nutzen und Belastung verdichten | festen Entry erzeugen |
| `contact_learning_state` | Memory/Sprache | Semantik | Zustand der Kontakt-Erfahrung benennen | absolute Wahrheit sein |
| `positive_return_pressure` | Regulation | Neurochemie | Rückführung positiver Überdehnung | Aktion blockieren |

### Entry-Geometrie-Kopplung

| Variable | Ebene | Rezeptor | Wirkung | Darf nicht |
|---|---|---|---|---|
| `entry_geometry_state` | Handlungsvorstufe | Kopplung | zeigen, ob aus Kontaktangebot bereits Entry-Geometrie reift | Strategie sein |
| `entry_geometry_bearing` | Handlungsvorstufe | Kopplung | Tragnaehe fuer konkrete Entry-Geometrie verdichten | Value-Gate ersetzen |
| `pre_geometry_thought_bearing` | Denken | Thought | Gedankennaehe vor Order-Geometrie tragen | Realitaet ersetzen |
| `pre_geometry_felt_bearing` | Fuehlen | MCM-Feld | Feldnaehe vor Order-Geometrie tragen | Form ersetzen |
| `pre_geometry_reality_bearing` | Realitaetspruefung | Weltkontakt | Realitaetsbindung vor Order-Geometrie tragen | Zukunft beweisen |
| `pre_geometry_preference_bearing` | Memory | Erfahrung | gelernte Kontaktpraeferenz vor Order-Geometrie tragen | Entry erzwingen |
| `organic_contact_bearing` | Handlungsvorstufe | Kontakt | natuerlich tragenden Bereichskontakt vor Entry-Geometrie zeigen | Impuls-Entry sein |

### Sinnes-Synchronisation

| Variable | Ebene | Rezeptor | Wirkung | Darf nicht |
|---|---|---|---|---|
| `sensory_sync_state` | Wahrnehmung | Sehen/Hoeren/Fuehlen/Zeit | gemeinsame Bindung der Sinneskanäle beschreiben | Entry-Regel sein |
| `visual_hearing_fit` | Wahrnehmung | Sehen/Hoeren | prüfen, ob Klang zur sichtbaren Form passt | Klang als Form ersetzen |
| `visual_felt_fit` | Wahrnehmung | Sehen/Fuehlen | prüfen, ob MCM-Feldwirkung zur Form passt | Feld als Sicht ersetzen |
| `hearing_felt_fit` | Wahrnehmung | Hoeren/Fuehlen | prüfen, ob Klang und Feldlage zusammenpassen | Druck automatisch tragen |
| `temporal_visual_fit` | Wahrnehmung | Zeit/Sehen | prüfen, ob Nachhall/Flow zur sichtbaren Form passt | Zukunft beweisen |
| `sensory_sync` | Wahrnehmung | multisensorisch | gebundene Sinneskohärenz verdichten | Value-Gate ersetzen |
| `sensory_desync_pressure` | Wahrnehmung/Regulation | multisensorisch | auseinanderlaufende Sinneslage als Druck zeigen | harte Sperre sein |
| `multisensory_binding_state` | Wahrnehmung/Sprache | Semantik | Bindungszustand benennen | Strategie sein |

### Memory und Formsprache

| Variable | Ebene | Rezeptor | Wirkung | Speicherpfad |
|---|---|---|---|---|
| `form_symbol_contact_maturity` | Memory | Memory/Formsymbol | gereifter Kontakt | reales Memory |
| `form_symbol_contact_utility` | Memory | Memory/Formsymbol | nutzbarer Kontaktwert | reales Memory |
| `form_symbol_contact_pain_memory` | Memory | Memory/Formsymbol | belastende Konsequenzspur | reales Memory |
| `form_symbol_action_trust` | Memory | Memory/Formsymbol | Handlungstragfähigkeit | reales Memory |
| `form_symbol_caution_trust` | Memory | Memory/Formsymbol | vorsichtige Gegenspur | reales Memory |
| `dio_syntax_density` | Sprache | Semantik | Bedeutungsdichte | Sprachmemory |
| `dio_syntax_compression` | Sprache | Semantik | Rohdatenverdichtung | Sprachmemory |
| `dio_syntax_origin` | Sprache | Semantik | eigene/gemischte/geliehene Herkunft | Sprachmemory |

### Hypothesen und Möglichkeiten

| Variable | Ebene | Rezeptor | Wirkung | Darf nicht |
|---|---|---|---|---|
| `possibility_observer_state` | Thought | Thought | Beobachterhaltung lesbar machen | Handlung auslösen |
| `possibility_observation_depth` | Thought/Raumzeit | Thought | Beobachtungstiefe zeigen | Reife vortäuschen |
| `possibility_reality_contact` | Realitätsprüfung | Thought | Kontakt zur Realität prüfen | Beweis ersetzen |
| `possibility_variant_maturity` | Thought/Memory | Thought | Variantenreife aus Wiederkehr | Strategie erzwingen |
| `possibility_variant_trust` | Thought/Memory | Thought | Vertrauen in Variante | Value-Gate ersetzen |
| `possibility_variant_caution` | Thought/Regulation | Thought | vorsichtige Gegenladung | Hypothese löschen |
| `hypothesis_trust_score` | Thought-Memory | Thought | bestätigte Hypothesenfamilie tragen | Realität ersetzen |
| `hypothesis_frustration_risk` | Thought/Regulation | Thought | Frust-/Distanzdruck zeigen | Denken abwerten |

### Neurochemie

| Variable | Ebene | Rezeptor | Wirkung | Darf nicht |
|---|---|---|---|---|
| `dopamine_tone` | Neurochemie | Neurochemie | Erwartung, Antrieb, Suchbewegung | Kauf-/Verkaufssignal sein |
| `noradrenaline_arousal` | Neurochemie | Neurochemie | Wachheit, Salienz, Alarm | Panikregel sein |
| `acetylcholine_focus` | Neurochemie | Neurochemie | Fokus, sensorischer Zoom | Tunnelblick erzwingen |
| `serotonin_stability` | Neurochemie | Neurochemie | Stabilität, Geduld, Ordnung | Lage blind beruhigen |
| `gaba_inhibition` | Neurochemie | Neurochemie | Hemmung, Dämpfung, Abstand | starre Sperre sein |
| `cortisol_load` | Neurochemie | Neurochemie | Stress, Belastung, Schutzspannung | Verlustregel sein |
| `endorphin_relief` | Neurochemie | Neurochemie | Entlastung, Druckabbau | Profitbelohnung allein sein |
| `glutamate_activation` | Neurochemie | Neurochemie | Aktivierung, Lernanstoß | Übererregung ignorieren |
| `neurochemical_balance` | Neurochemie | Neurochemie | Last/Support-Bilanz | Entscheidung ersetzen |

### Position und Konsequenz

| Variable | Ebene | Rezeptor | Wirkung | Speicherpfad |
|---|---|---|---|---|
| `position_cognitive_load` | Position | Position | Denklast einer offenen Position | Outcome-Zusammenfassung |
| `exit_decision_pressure` | Position | Position | Druck aktiver Exit-Bewertung | Outcome/Regulation |
| `position_mcm_field_strain` | Position | Position | Feldbelastung durch Beteiligung | Outcome |
| `position_self_trust_gap` | Position | Position | Lücke im Selbstvertrauen | Thought/Outcome |
| `position_process_quality` | Position | Position | Qualität des Umgangs | Memory/Thought-Memory |
| `position_consequence_burden` | Konsequenz | Outcome | Belastung aus Ergebnis | reales Memory |
| `position_constructive_bearing` | Konsequenz | Outcome | konstruktive Tragwirkung | reales Memory |
| `packet_process_reward` | Konsequenz | Outcome | Prozessqualität positiv tragen | Memory/Neurochemie |
| `packet_reorganization_need` | Konsequenz | Outcome | Reorganisation anfordern | Thought/Regulation |

### Entry-Kontaktpraeferenz

| Variable | Ebene | Rezeptor | Wirkung | Darf nicht |
|---|---|---|---|---|
| `entry_contact_learning` | Memory | Konsequenz | reale Entry-Kontakte verdichten | Strategie ersetzen |
| `entry_contact_preference_memory` | Memory | Erfahrung | Kontaktvertrauen persistent tragen | hartes Gate werden |
| `selected_entry_preference_key` | Handlung | Kontakt | gelernte Kontaktlage benennen | Entry erzwingen |
| `selected_entry_preference_trust` | Handlung/Memory | Vertrauen | tragende Folgeerfahrung mitsprechen lassen | Realitaet ersetzen |
| `selected_entry_preference_caution` | Handlung/Memory | Vorsicht | belastende Folgeerfahrung mitsprechen lassen | Handlung verbieten |
| `selected_entry_preference_maturity` | Handlung/Memory | Reife | wiederholte Kontaktnaehe einordnen | fixe Schwelle sein |
| `selected_entry_preference_utility` | Handlung/Memory | Nutzen | konstruktive Kontaktwirkung tragen | Profit-Regel sein |
| `property_profiles` | Memory | reale Konsequenz | aehnliche Eigenschaftsraeume aus Outcome lernen | Hypothese oder Strategie sein |
| `selected_entry_property_profile_id` | Handlung/Memory | Profilbezug | gewaehltes reales Eigenschaftsprofil sichtbar machen | Entry erzwingen |
| `selected_entry_property_profile_similarity` | Handlung/Memory | Aehnlichkeit | neue Kontaktlage mit realem Profil vergleichen | feste Schwelle sein |
| `selected_entry_property_profile_trust` | Handlung/Memory | Vertrauen | tragende Profile weich mitsprechen lassen | Profit beweisen |
| `selected_entry_property_profile_caution` | Handlung/Memory | Vorsicht | belastende Profile weich mitsprechen lassen | Handlung verbieten |
| `selected_entry_property_profile_maturity` | Handlung/Memory | Reife | wiederholte Eigenschaftsnaehe einordnen | fixe Regel sein |
| `selected_entry_property_profile_utility` | Handlung/Memory | Nutzen | konstruktive Profile weich tragen | Value-Gate ersetzen |
| `selected_memory_caution_pressure` | Memory/Handlung | vorsichtige Rueckfuehrung | belastete Erfahrung als koerperliche Vorsicht tragen | harte Sperre sein |
| `selected_memory_bearing_pressure` | Memory/Handlung | tragende Rueckfuehrung | tragende Erfahrung als weiche Naehe tragen | Entry erzwingen |
| `mature_careful_contact_pressure` | Memory/Regulation | reife Vorsicht | bekannte, aber belastete Kontaktreife in Abstand uebersetzen | reife Tragfaehigkeit sein |
| `long_return_area_upper_contact` | Handlung/Wahrnehmung | Kontaktlage | Raeumliche Rueckkehrnaehe fuer LONG benennen | Strategie sein |
| `short_return_area_lower_contact` | Handlung/Wahrnehmung | Kontaktlage | Raeumliche Rueckkehrnaehe fuer SHORT benennen | Strategie sein |

### Raumzeit, Nachhall und Doppler

| Variable | Ebene | Rezeptor | Wirkung | Darf nicht |
|---|---|---|---|---|
| `subconscious_afterimage_pressure` | Raumzeit/MCM | Nachhall | unbewussten Restdruck zeigen | Gegenwart ersetzen |
| `world_motion_afterimage_strength` | Raumzeit | Nachhall | Restbild bewegter Welt | harte Vorhersage sein |
| `motion_approach_pressure` | Raumzeit | Nachhall | näherrückende Restspur | Entry erzwingen |
| `motion_recession_pressure` | Raumzeit | Nachhall | abklingende Restspur | Entwarnung erzwingen |
| `contact_frequency_shift` | Raumzeit/Hören | Nachhall | Rhythmusänderung zeigen | Signalregel sein |
| `future_variant_pressure` | Thought/Raumzeit | Nachhall | Vorhall möglicher Fortsetzung | Zukunft beweisen |
| `afterimage_doppler_bias` | Raumzeit | Nachhall | gerichtete Verschiebung | Richtung erzwingen |

## Aktive Prüfpflichtige Kaskaden

### Last-Kaskade

```text
Position/Thought/Neurochemie
-> nervous_system_load
-> distance_level / reflection_pull
-> keine harte Sperre
```

Prüfen: Wird dieselbe Last doppelt in Regulation addiert?

### Reorganisations-Kaskade

```text
Thought mismatch
-> reality_check_need
-> reorganization_pressure
-> Thought-Memory / Regulation
```

Prüfen: Wird eine Hypothese fälschlich als Realität gespeichert?

### Tragfähigkeits-Kaskade

```text
Form/MCM/Memory passt
-> maturity / trust
-> Handlungstiefe steigt weich
-> Value-Gate bleibt einzige harte Prüfung
```

Prüfen: Wird Vertrauen direkt zu Entry, statt nur Handlungstiefe zu modulieren?

### Nachhall-Kaskade

```text
bewegte Welt
-> afterimage
-> Doppler/Vorhall
-> Variantenraum
-> Thought, nicht Handlung
```

Prüfen: Wird Vorhall als Vorhersage missverstanden?

### Sinnesbalance-Kaskade

```text
Sehen
-> Hoeren
-> Fuehlen
-> Denken
-> Handlungsnaehe
-> Value-Gate
```

Pruefen: Kippt DIO wegen unscharfer Form, zu starkem Hoerreiz, schwachem
MCM-Fuehlen, unklarer Hypothese oder fehlender Handlungsnaehe?

Aktive Diagnose:

| Feld | Ebene | Zweck | Darf nicht |
|---|---|---|---|
| `sensory_balance.sehen` | Wahrnehmung | Formklarheit lesen | Entry erzwingen |
| `sensory_balance.hoeren` | Wahrnehmung | Marktspannung als Klangreiz lesen | Handlung erlauben |
| `sensory_balance.fuehlen` | MCM-Feld | Tragfaehigkeit des Kontakts lesen | Realitaet ersetzen |
| `sensory_balance.denken` | Thought | Hypothesenverdichtung lesen | Gedanke als Tatsache speichern |
| `sensory_balance.handlung` | Handlung | Kopplung zur Entry-Naehe lesen | hartes Gate sein |
| `sensory_balance.break_layer` | Diagnose | Bruchstelle benennen | Regelpfad werden |

## Arbeitsregel

Neue Variablen werden nur aufgenommen, wenn sie:

1. eine klare Ebene haben,
2. einer Rezeptorfamilie zugeordnet sind,
3. einen Zielregler nennen,
4. einen Speicherpfad oder bewusst keinen Speicher haben,
5. klar sagen, was sie nicht dürfen.

Diese Datei ist damit die aktive Variablenordnung. Die alte
`MCM_VARIABLEN_MECHANIK.md` bleibt Archiv und wird nicht mehr direkt erweitert.
