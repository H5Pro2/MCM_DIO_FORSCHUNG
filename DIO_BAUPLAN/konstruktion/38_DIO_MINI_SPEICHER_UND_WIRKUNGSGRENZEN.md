# DIO_MINI Speicher und Wirkungsgrenzen

Diese Datei haelt fest, welche Schichten DIO_MINI aktuell besitzt und
welche Schichten passiv bleiben muessen.

Ziel:

```text
Keine Rueckkehr zu ueberladener Mechanik.
Keine Hypothese als Realitaet.
Keine Kontaktlage als Entry-Regel.
```

## Sensorik

Quelle:

```text
DIO_MINI\mini_world.py
DIO_MINI\mcm_neuron.py
```

Aufgabe:

```text
sehen
hoeren
fuehlen
```

Die Sensorik erzeugt eine kleine Weltwahrnehmung.
Sie ist noch kein Gedaechtnis und keine Strategie.

## Formwort

Quelle:

```text
DIO_MINI\semantic_memory.py
make_syntax_symbol
make_syntax_vector
```

Aufgabe:

```text
Eine wiederkehrende sensorische Lage bekommt ein DIO-eigenes Wort.
```

Beispiel:

```text
dio_14eb
dio_0szn
dio_0wv3
```

Grenze:

```text
Ein Formwort ist nicht die Realitaet.
Ein Formwort ist Wiedererkennung.
```

## Handlungserfahrung

Quelle:

```text
SemanticMemory.learn
SemanticMemory.learn_observation
```

Aufgabe:

```text
Handlung
Konsequenz
Timingnaehe
Beobachtungslernen
```

Diese Schicht ist die einzige Mini-Schicht, die aktuell in
`choose_action` gelesen wird.

Wichtig:

```text
Das ist der aktive Lernkern.
Hier entsteht Handlungserfahrung.
```

## Kontaktlagen

Quelle:

```text
contact_lagen
DIO_MINI\build_contact_reference_protocol.py
DIO_MINI\store_contact_lagen.py
DIO_MINI\report_contact_lagen.py
```

Aufgabe:

```text
Beschreiben, in welcher Art von Weltbegegnung eine Erfahrung entstand.
```

Aktuelle Kontaktlagen:

```text
exakte_wiederbegegnung
nahe_aehnlichkeit
ferne_aehnlichkeit
konflikt_wiederbegegnung
bestaetigte_sensorvarianz
verschobene_sensorvarianz
```

Grenze:

```text
Kontaktlagen sind passiv.
Sie duerfen nicht direkt von choose_action gelesen werden.
```

## Satzspuren

Quelle:

```text
sentence_traces
DIO_MINI\build_contact_sentence_trace.py
DIO_MINI\store_sentence_traces.py
DIO_MINI\report_sentence_traces.py
```

Aufgabe:

```text
Kontaktwort + Formwort + Erleben + Konsequenznaehe
```

Beispiel:

```text
dio_contact_0w23dz5 + dio_14eb -> kontakt_handlung_bestaetigt
```

Grenze:

```text
Satzspuren sind passiv.
Sie duerfen nicht direkt Handlung ausloesen.
```

## Lesewerkzeuge

Aktuelle passive Leser:

```text
DIO_MINI\read_form_sentence_traces.py
DIO_MINI\read_sentence_conflicts.py
DIO_MINI\report_experience_landscape.py
DIO_MINI\read_stable_direction_traces.py
```

Aufgabe:

```text
Erfahrung lesbar machen.
Konflikte sichtbar machen.
Stabile Richtungsspuren sichtbar machen.
Beobachtung von Bestaetigung trennen.
```

Grenze:

```text
Lesewerkzeuge sind Diagnose.
Sie sind nicht Motorik.
```

## Aktive Handlung

Quelle:

```text
DIO_MINI\run_mini.py
choose_action
```

Aktuell gelesen:

```text
action_diagnostics
readiness
action_bias
WAIT-Bias
vorsichtige Reifungs-/Signalschwelle im Mini-Kern
```

Wichtig:

```text
Aktive Handlung entsteht aus aktueller Feldreaktion plus gelernter
Handlungserfahrung.
```

Nicht gelesen:

```text
contact_lagen
sentence_traces
experience_landscape
stable_direction_traces
reflection_seeds
```

## Fachliche Grenze

Zulaessig:

```text
Wahrnehmen
Handeln
Konsequenz speichern
Kontaktlage nachtraeglich protokollieren
Satzspur passiv verdichten
Konflikte passiv lesen
Stabilitaet passiv lesen
Reflexionskeime passiv speichern
```

Nicht zulaessig:

```text
Wenn Kontaktlage X, dann Trade.
Wenn Satzspur X positiv, dann Entry.
Wenn stabile Richtung X, dann automatisch handeln.
Wenn Reflexionskeim X bestaetigt, dann automatisch handeln.
```

## Passive Reflexionskeime

Neue Speicherschicht:

```text
reflection_seeds
```

Quelle:

```text
DIO_MINI\build_passive_reflection_layer.py
DIO_MINI\store_reflection_seeds.py
DIO_MINI\report_reflection_seeds.py
```

Fachlicher Inhalt:

```text
Eine Formfamilie wurde:

1. beobachtet,
2. spaeter bestaetigt gehandelt,
3. im Folgelauf erneut bestaetigt.
```

Aktuell gespeicherte Keime:

```text
dio_reflect_11nxj7w:
  family: dio_0hd3
  state: reflection_seed_reconfirmed
  followup_reward: 5.837140

dio_reflect_01hi6xw:
  family: dio_0c6o
  state: reflection_seed_reconfirmed
  followup_reward: 4.592656

dio_reflect_1bdledh:
  family: dio_1wie
  state: reflection_seed_reconfirmed
  followup_reward: 0.794658
```

Grenze:

```text
reflection_seeds sind passive Selbstwahrnehmung.
Sie werden nicht von action_diagnostics gelesen.
Sie werden nicht von choose_action gelesen.
Sie sind kein Entry-System.
```

Passivitaetspruefung:

```text
debug\dio_mini_reflection_passivity_check
```

Vergleich:

```text
Memory mit reflection_seeds:
  RUN 133
  trades: 3
  reward: 3.4042

Memory ohne reflection_seeds:
  RUN 133
  trades: 3
  reward: 3.4042
```

Dateipruefung:

```text
episodes.csv Hash identisch:
5FE9E7422F4AADE40ED2DB2BA458EDB3237D7FAF83EEB1AEA027C0DDA17F8E19
```

Befund:

```text
reflection_seeds sind praktisch passiv bestaetigt.
Sie veraendern den aktuellen Mini-Handlungspfad nicht.
```

Selbstwahrnehmungslesung:

```text
DIO_MINI\report_reflection_self_awareness.py
debug\dio_mini_reflection_self_awareness_v1
```

Ergebnis:

```text
self_awareness_stable:
  count: 2
  families: dio_0c6o, dio_0hd3
  followup_reward_sum: 10.429796

self_awareness_tentative:
  count: 1
  family: dio_1wie
  followup_reward_sum: 0.794658
```

Grenze:

```text
self_awareness_stable ist keine Handlungsfreigabe.
Es ist nur eine passiv lesbare Selbstwahrnehmungsspur.
```

## Aktueller Befund

Nach Probe13:

```text
sentence_traces: 93
families: 66
reflection_seeds: 3
self_awareness_stable: 2
self_awareness_tentative: 1

kontaktlagenuebergreifend_bestaetigt: 2
lokal_bestaetigt: 12
conflict_or_burden: 1
```

Stabil:

```text
dio_14eb -> SHORT ueber 3 Kontaktlagen
dio_0szn -> SHORT ueber 3 Kontaktlagen
```

Konflikt:

```text
dio_0wv3
```

## Naechster sinnvoller Ausbau

Nicht neue Motorik.

Zuerst:

```text
Aktive Handlungserfahrung im Mini-Kern sauber dokumentieren:
Welche Werte liest choose_action?
Welche Werte sind organisch notwendig?
Welche Werte sind nur historische Altlast?
```

Danach kann entschieden werden, ob passive Leseschichten spaeter in eine
Reflexionsschicht duerfen.

Stand jetzt:

```text
Eine passive Reflexionsschicht ist vorhanden und in der Memory speicherbar.
Sie bleibt getrennt von aktiver Handlung.
```

## Transfer stabiler Selbstwahrnehmung

Umgesetzt:

```text
DIO_MINI\report_self_awareness_transfer.py
```

Zweck:

```text
Pruefen, ob passive Selbstwahrnehmungsfamilien in einem spaeteren,
leicht veraenderten Probe-Lauf wieder auftauchen.
```

Wichtig:

```text
Der Report liest nur.
Er schreibt nicht in Memory.
Er wirkt nicht auf choose_action.
Er wirkt nicht auf score_long, score_short oder score_wait.
```

Probe14-Befund:

```text
dio_0hd3:
  transfer_reconfirmed_clean
  reward_sum: 6.10438

dio_0c6o:
  transfer_not_seen

dio_1wie:
  transfer_not_seen
```

Fachliche Grenze:

```text
Eine Selbstwahrnehmungsspur darf nicht automatisch Handlung werden.
Sie sagt nur:
"Diese Erfahrung erkenne ich wieder"
oder:
"Diese Erfahrung ist in dieser Welt nicht aktiv."
```

Das verhindert Tagtraeumerei:

```text
Gedanke/Erinnerung != aktuelle Realitaet.
Aktuelle Sensorlage muss eigenstaendig gesehen, gehoert und gefuehlt werden.
```

## Passive Reflexionskarte

Umgesetzt:

```text
DIO_MINI\report_self_awareness_reflection_map.py
```

Die Reflexionskarte verdichtet alte passive Reflexionskeime gegen eine neue
Weltlage:

```text
reflection_memory_reconfirmed:
  alte Spur wird gesehen und getragen

reflection_memory_quiet:
  alte Spur bleibt in dieser Welt still

reflection_memory_observed:
  alte Spur wird gesehen, aber nicht gehandelt

reflection_memory_conflict:
  alte Spur wird gesehen, aber nicht getragen
```

Probe14:

```text
dio_0hd3:
  reflection_memory_reconfirmed
  "Ich erkenne eine alte Spur wieder und der Kontakt traegt."

dio_0c6o:
  reflection_memory_quiet
  "Ich kenne diese Spur, aber diese Welt ruft sie gerade nicht auf."

dio_1wie:
  reflection_memory_quiet
  "Ich kenne diese Spur, aber diese Welt ruft sie gerade nicht auf."
```

Speichergrenze:

```text
Die Reflexionskarte ist aktuell kein gespeicherter Motorikzustand.
Sie ist ein Bericht ueber Selbstwahrnehmung und Realitaetstrennung.
```

## Kontextabhaengige Erinnerung bestaetigt

Probe14 und Probe15 zeigen zusammen:

```text
Eine Erinnerung darf still sein.
Eine Erinnerung darf spaeter wieder aktiv werden.
Eine Erinnerung darf nicht automatisch als Realitaet behandelt werden.
```

Konkreter Befund:

```text
dio_0c6o:
  Probe14: quiet
  Probe15: reconfirmed

dio_0hd3:
  Probe14: reconfirmed
  Probe15: reconfirmed

dio_1wie:
  Probe14: quiet
  Probe15: quiet
```

Damit wird die Speichergrenze fachlich schaerfer:

```text
Memory traegt Erfahrung.
Aktuelle Sensorik entscheidet, ob diese Erfahrung in der Welt beruehrt wird.
Reflexion benennt den Kontakt.
Motorik bleibt getrennt.
```

## Konfliktfaehige Erinnerung bestaetigt

Probe16 zeigt die Gegenrichtung:

```text
Eine bekannte Spur kann gesehen werden,
aber der aktuelle Weltkontakt traegt die alte Handlungsnaehe nicht.
```

Konkreter Verlauf:

```text
dio_0c6o:
  erst LONG negativ gegen die neue Welt
  danach SHORT positiv durch Konsequenzlernen
  Reflexionskarte: reflection_memory_conflict
```

Speichergrenze:

```text
Der Konflikt wird nicht als harte Regel gespeichert.
Er wird als passive Lesung festgehalten:
"Diese alte Spur ist in dieser Welt nicht identisch tragend."
```

Damit sind drei passive Speicherzustaende belegt:

```text
reflection_memory_quiet:
  Erinnerung vorhanden, aktuelle Welt ruft sie nicht.

reflection_memory_reconfirmed:
  Erinnerung wird gesehen und getragen.

reflection_memory_conflict:
  Erinnerung wird gesehen, aber der aktuelle Kontakt traegt sie nicht.
```

Zusammenfassung:

```text
DIO_MINI\report_reflection_validation.py
```

Validierter Stand Probe14 bis Probe16:

```text
quiet:
  belegt

reconfirmed:
  belegt

conflict:
  belegt
```

Speicherentscheidung offen:

```text
Die Reflexionskarte ist aktuell Auswertung.
Sie wird noch nicht als dauerhafte Memory-Schicht zurueckgeschrieben.
```

Aktualisierung:

```text
Die Reflexionskarte ist jetzt als passive Memory-Schicht speicherbar.
```

Umgesetzt:

```text
SemanticMemory.reflection_maps
DIO_MINI\store_reflection_maps.py
```

Speicherinhalt:

```text
reflection_map_symbol
reflection_symbol
symbol_family
reflection_map_state
reflection_map_reason
dio_sentence
seen_count
executed_count
observed_count
reward_sum
source_probe
passive_only
```

Wirkungsgrenze:

```text
reflection_maps werden nicht von action_diagnostics gelesen.
reflection_maps werden nicht von choose_action gelesen.
reflection_maps veraendern score_long, score_short und score_wait nicht.
```

Passivitaet geprueft:

```text
mit reflection_maps == ohne reflection_maps
episodes.csv Hash identisch
```

## Familienakte als passive Speicherlesung

Aktualisierung:

```text
DIO_MINI\report_family_file.py
```

Zweck:

```text
Eine Familie wird nicht nur als Aktion gelesen.
Sie wird als Akte gelesen:

Was wurde getan?
Was wurde nur beobachtet?
Welche Kontaktlagen gab es?
Welche Satzspuren wurden gespeichert?
Welche Reflexionskeime existieren?
Welche Reflexionskarten wurden spaeter still, getragen oder konflikthaft?
```

Wichtig:

```text
Die Familienakte ist ein Bericht.
Sie schreibt keine Memory.
Sie wird nicht von choose_action gelesen.
Sie erzeugt keine Handlung, keinen Block und keine Richtung.
```

Damit bleibt die Grenze sauber:

```text
Realitaet / Handlung:
  Mini-DIO lernt aus Kontakt und Konsequenz.

Reflexion / Kortex-Vorstufe:
  Mini-DIO kann nachtraeglich lesen, was eine Familie passiv bedeutet.
```

## Familien-Zeitlinie

Aktualisierung:

```text
DIO_MINI\report_family_reflection_timeline.py
```

Zweck:

```text
reflection_maps werden pro Familie zeitlich gelesen.
Dadurch wird sichtbar, ob eine Familie:

still bleibt,
wieder getragen wird,
in Konflikt geraet,
oder gemischt ueber mehrere Welten erscheint.
```

Beispiel:

```text
dio_0c6o:
  quiet -> reconfirmed -> conflict

dio_0hd3:
  reconfirmed -> reconfirmed -> quiet

dio_1wie:
  quiet
```

Grenze:

```text
Auch diese Zeitlinie ist passiv.
Sie beschreibt DIOs gespeicherte Erfahrungslandschaft.
Sie entscheidet nicht.
```

## Passive Kortexansicht

Aktualisierung:

```text
DIO_MINI\report_passive_cortex_view.py
```

Zweck:

```text
Die passive Kortexansicht verbindet gespeicherte Akte und aktuelle Welt:

Familienakte:
  was wurde gespeichert?

Familien-Zeitlinie:
  wie kehrte die Familie ueber Welten wieder?

Aktuelle Debug-Welt:
  wird die Familie gerade gesehen?
  wird gehandelt?
  ist die aktuelle Konsequenz tragend oder konflikthaft?
```

Grenze:

```text
Die Kortexansicht liest.
Sie schreibt keine Memory.
Sie wird nicht in choose_action eingespeist.
Sie erzeugt keine Strategie und kein Gate.
```

Fachlicher Nutzen:

```text
Sie macht sichtbar, ob DIO eine gespeicherte Familie aktuell:

nicht sieht,
still sieht,
getragen sieht,
oder konflikthaft erlebt.
```

## Passive Kortexdiagnose ueber mehrere Welten

Aktualisierung:

```text
DIO_MINI\report_passive_cortex_comparison.py
```

Zweck:

```text
Mehrere passive Kortexansichten werden nebeneinander gelesen.
Damit entsteht keine neue Handlungsschicht, sondern eine Diagnose:

Welche Familie wurde in welcher Welt gesehen?
Welche Familie wurde getragen?
Welche Familie wurde konflikthaft?
Welche Familie blieb still?
```

Validierter Stand Probe14 bis Probe16:

```text
dio_0c6o:
  not_seen -> seen_carried -> seen_conflict

dio_0hd3:
  seen_carried -> seen_carried -> not_seen

dio_1wie:
  not_seen -> not_seen -> not_seen
```

Wirkungsgrenze:

```text
Auch der Vergleich ist passiv.
Er ist kein Gate, kein Strategy-Modul und kein Trade-Ausloeser.
```

## Standard-Diagnoseblock

Aktualisierung:

```text
DIO_MINI\run_passive_cortex_diagnostics.py
```

Zweck:

```text
Ein einzelner Diagnoseaufruf erzeugt die passive Lesekette:

Familienakte
Familien-Zeitlinie
Kortexansicht je Probe
Kortexvergleich ueber Proben
Familien-Reifeverlauf ueber Proben
```

Wichtig:

```text
Der Standard-Diagnoseblock ist keine neue Speicher- oder Handlungsschicht.
Er fasst nur bestehende passive Speicher- und Debuginformationen zusammen.
```

Beispielaufruf:

```text
python -m DIO_MINI.run_passive_cortex_diagnostics ^
  --memory bot_memory\dio_mini_sensor_relation_probe5_variation_memory.json ^
  --probe probe14=debug\dio_mini_probe14_self_awareness_shift\run ^
  --probe probe15=debug\dio_mini_probe15_self_awareness_return\run ^
  --probe probe16=debug\dio_mini_probe16_self_awareness_conflict\run ^
  --family dio_0c6o ^
  --family dio_0hd3 ^
  --family dio_1wie ^
  --output-dir debug\dio_mini_passive_cortex_standard_probe14_16
```

Grenze:

```text
Kein Memory-Schreiben.
Kein choose_action.
Keine Motorik.
Keine harte Regel.
```

Erweiterung:

```text
Wenn mehrere Proben uebergeben werden, erzeugt der Standard-Diagnoseblock
jetzt zusaetzlich:

family_maturation_path/
  dio_mini_family_maturation_path.csv
  dio_mini_family_maturation_path_detail.csv
  dio_mini_family_maturation_path.json
  dio_mini_family_maturation_path.md

family_maturation_reflection/
  dio_mini_family_maturation_reflection.csv
  dio_mini_family_maturation_reflection.json
  dio_mini_family_maturation_reflection.md

passive_inner_awareness/
  dio_mini_passive_inner_awareness.csv
  dio_mini_passive_inner_awareness_summary.csv
  dio_mini_passive_inner_awareness.json
  dio_mini_passive_inner_awareness.md

passive_inner_state_<probe>/
  dio_mini_passive_inner_state_protocol.csv
  dio_mini_passive_inner_state_protocol_summary.csv
  dio_mini_passive_inner_state_protocol.json
  dio_mini_passive_inner_state_protocol.md

passive_inner_timeline_<probe>/
  dio_mini_passive_inner_state_timeline.csv
  dio_mini_passive_inner_state_timeline_summary.csv
  dio_mini_passive_inner_state_timeline.json
  dio_mini_passive_inner_state_timeline.md

passive_inner_stability_<probe>/
  dio_mini_passive_inner_stability_detail.csv
  dio_mini_passive_inner_stability_overview.csv
  dio_mini_passive_inner_stability_transitions.csv
  dio_mini_passive_inner_stability.json
  dio_mini_passive_inner_stability.md

passive_inner_coherence_<probe>/
  dio_mini_passive_inner_coherence_map_detail.csv
  dio_mini_passive_inner_coherence_map_summary.csv
  dio_mini_passive_inner_coherence_map.json
  dio_mini_passive_inner_coherence_map.md

dio_mini_passive_inner_coherence_transfer/
  dio_mini_passive_inner_coherence_transfer_detail.csv
  dio_mini_passive_inner_coherence_transfer_by_world.csv
  dio_mini_passive_inner_coherence_transfer_summary.csv
  dio_mini_passive_inner_coherence_transfer.json
  dio_mini_passive_inner_coherence_transfer.md

dio_mini_passive_cortex_diagnostics_summary.json
dio_mini_passive_cortex_diagnostics_summary.md
```

Grenze:

```text
Auch dieser integrierte Reifeverlauf bleibt passiv.
Er liest nur vorhandene Debug-/Memory-Spuren.
Er schreibt keine Memory.
Er beeinflusst keine Handlung.

Die Summary-Dateien sind nur ein Inhaltsverzeichnis mit Kurzbefund.

Die Reflexionshaltung liest nur:
  getragen gereift
  stabil getragen
  offene Beobachtung
  Vorsicht nach Konflikt
  gehalten/offen

Sie ist keine Handlungsempfehlung.

Die passive Innenwahrnehmung verdichtet diese Haltungen zu:
  inner_carried
  inner_cautious
  inner_open_observation
  inner_unfinished
  inner_cooling
  inner_open

Auch diese Innenwahrnehmung ist nur Lesbarkeit.
Sie ist noch kein innerer Motorimpuls.

Das passive Innenlage-Protokoll verbindet diese Innenwahrnehmung pro Probe
mit den Episoden:
  inner_state
  contact_state
  action
  reward
  sehen/hoeren/fuehlen-Ausschnitt

Es zeigt:
  wann eine Familie innen getragen war
  wann sie vorsichtig/offen blieb
  ob daraus realer Kontakt, Beobachtung oder gehaltene Spannung wurde

Auch dieses Protokoll bleibt Diagnose.

Die passive Innenlage-Zeitlinie verdichtet das Protokoll chronologisch:
  timeline_start
  same_inner_state
  inner_carried_to_inner_open_observation
  inner_open_observation_to_inner_cautious
  inner_cautious_to_inner_unknown
  inner_unknown_to_inner_carried

Damit wird sichtbar, ob DIO Mini im Lauf von getragen zu offen,
von offen zu vorsichtig oder zurueck zu getragen wechselt.

Auch diese Zeitlinie ist keine Steuerung.

Die passive Innenlage-Stabilitaet beantwortet:
  kommt positiver Kontakt aus stabiler Innenlage?
  kommt positiver Kontakt aus Rueckkehr in getragene Innenlage?
  bleiben offene/vorsichtige Innenlagen Beobachtung?

Sie trennt:
  stable_state
  transition_state
  start_state

und:
  positive_real_contact
  negative_real_contact
  observed_potential
  quiet

Auch diese Auswertung ist nur Diagnose.

Die passive Innenlage-Kohaerenzkarte verbindet pro Familie:
  inner_state
  contact_quality
  sehen_form_flow
  sehen_form_stability
  hoeren_energy_tone
  fuehlen_mcm_coherence
  fuehlen_mcm_tension
  reward / best_reward

Wichtig:
  inner_carried ist nicht einfach der hoechste Sichtwert
  und nicht einfach die hoechste MCM-Kohaerenz.

Getragenheit entsteht als gelesene Kopplung aus Familie,
Innenlage, Kontakt und Konsequenz.

Auch diese Karte ist passiv.

Der passive Innenlage-Kohaerenz-Transfer vergleicht mehrere Welten.
Er liest, ob ein Innenzustand wie inner_carried in verschiedenen Welten
mit aehnlicher Kontaktqualitaet auftritt.

Er darf nur sagen:
  diese Kopplung erscheint in mehreren Welten
  diese Kopplung traegt dort positiv
  diese Kopplung bleibt dort Beobachtung
  diese Kopplung hat Ausnahmen / Konfliktspuren

Er darf nicht sagen:
  ab jetzt immer handeln
  ab jetzt blockieren
  ab jetzt Gate setzen
```

## Reflection-Map-Provenienz

Korrektur:

```text
make_reflection_map_symbol beruecksichtigt jetzt source_probe.
```

Warum:

```text
Eine stille Rueckkehr in probe16 und eine stille Rueckkehr in probe17
duerfen nicht dieselbe passive Karte ueberschreiben.

Die Herkunft ist Teil der gespeicherten passiven Akte.
```

Ergebnis:

```text
dio_0c6o:
  probe14 quiet
  probe15 reconfirmed
  probe16 conflict
  probe17 quiet

dio_0hd3:
  probe14 reconfirmed
  probe15 reconfirmed
  probe16 quiet
  probe17 quiet

dio_1wie:
  probe16 quiet
  probe17 quiet
```

Grenze:

```text
Auch diese Provenienz bleibt passiv.
Sie verbessert Lesbarkeit und verhindert Speicherueberschreibung.
Sie erzeugt keine Handlung.
```

## Probe-Wiederholung als passive Reifelesung

Probe17 wurde nach gespeicherter Probe17-Erfahrung erneut ausgefuehrt.

Beobachtung:

```text
Erster Probe17-Kontakt:
  zuerst zwei stille Laeufe,
  danach neue tragende Familien.

Probe17-Wiederholung:
  vier Laeufe direkt stabil,
  jedes Mal 3 Trades,
  jedes Mal derselbe Reward.
```

Passiv wiedergetragen:

```text
dio_0ofo
dio_04z7
dio_1bwb
```

Passiv nicht erneut getragen:

```text
dio_0n9e
```

Nur beobachtet oder gehalten:

```text
dio_14xc
dio_1k7y
dio_1mym
```

Grenze:

```text
Diese Lesung sagt nicht:
  diese Familie muss handeln.

Sie sagt nur:
  diese Familie wurde ueber Wiederholung stabil,
  instabil,
  still,
  beobachtet
  oder gehalten gelesen.
```

Speicherwirkung:

```text
Die aktive Wirkung entsteht weiterhin nur aus:
  action_diagnostics
  echter Konsequenz
  beobachteter Wiederkehr
  symbolischer Verdichtung

Nicht aus:
  Kortexvergleich
  Familienakte
  Reflexionszeitlinie
  Repeat-Stability-Report
```

## Repeat-Stability-Report

Neuer passiver Leser:

```text
DIO_MINI/report_repeat_stability.py
```

Er liest:

```text
debug/**/episodes.csv
```

Er schreibt:

```text
dio_mini_repeat_stability.csv
dio_mini_repeat_stability.json
dio_mini_repeat_stability.md
```

Er erkennt passiv:

```text
repeat_executed_carried
repeat_partly_carried
repeat_held_pressure
repeat_observed_potential
repeat_executed_unresolved
repeat_seen_unclear
repeat_not_seen
```

Probe17-Wiederholung:

```text
dio_0ofo:
  repeat_executed_carried
  seen_runs=4
  executed_runs=4
  reward=5.812000

dio_04z7:
  repeat_executed_carried
  seen_runs=4
  executed_runs=4
  reward=4.347040

dio_1bwb:
  repeat_executed_carried
  seen_runs=4
  executed_runs=4
  reward=3.647524

dio_14xc:
  repeat_observed_potential

dio_1k7y:
  repeat_held_pressure

dio_1mym:
  repeat_observed_potential
```

Wirkungsgrenze:

```text
Der Repeat-Stability-Report ist eine passive Leseschicht.
Er darf nicht entscheiden.
Er darf nicht handeln.
Er darf nicht in choose_action einfliessen.
Er beschreibt nur, ob Wiederholung stabil, offen, gehalten oder beobachtet war.
```

## Familien-Kontrastreport

Neuer passiver Leser:

```text
DIO_MINI/report_family_contrast.py
```

Er liest:

```text
debug/**/episodes.csv
```

Er vergleicht pro Familie:

```text
Sehen:
  sehen_form_flow
  sehen_form_stability
  sehen_form_change

Hoeren:
  hoeren_energy_tone
  hoeren_energy_shift

Fuehlen:
  fuehlen_mcm_coherence
  fuehlen_mcm_tension
  fuehlen_mcm_asymmetry

Kognitive Naehe:
  trade_readiness
  associative_trade
  observation_trade_signal
  maturity_gap
  mature_transfer
  observation_learning_pressure
```

Er erkennt passiv:

```text
carried
conflict
held
observed
quiet
```

Wichtig:

```text
Der Report sagt nicht:
  wenn mcm_coherence hoch ist, dann trade.

Er zeigt nur:
  welche Sensorik und Feldlage bei welchen Familien
  mit welcher Konsequenz zusammen aufgetreten ist.
```

Probe18-Kontrast:

```text
carried:
  dio_0arw
  dio_1u7v
  dio_0akd
  dio_0120

observed:
  dio_14xc

conflict:
  dio_1vpi
```

Befund:

```text
dio_14xc und dio_1vpi haben beide:
  hohe visuelle Stabilitaet,
  hohe MCM-Kohaerenz,
  hohe MCM-Spannung.

Trotzdem:
  dio_14xc bleibt beobachtet.
  dio_1vpi handelt teilweise und ist negativ.

Damit ist klar:
Tragfaehigkeit ist nicht ein einzelner hoher Sensorwert.
Tragfaehigkeit entsteht aus Familienkontakt plus Konsequenzkopplung.
```

Wirkungsgrenze:

```text
Auch der Familien-Kontrastreport bleibt passiv.
Er darf keine Schwelle erzeugen.
Er darf kein Gate erzeugen.
Er darf keine Handlung korrigieren.
Er dient nur dazu, DIOs wiederkehrende Sensor-/Feld-/Konsequenzlagen lesbar zu machen.
```

## Familien-Reifeverlauf

Neuer passiver Leser:

```text
DIO_MINI/report_family_maturation_path.py
```

Er liest mehrere Debug-Wurzeln:

```text
probe18_first=debug\...
probe18_repeat1=debug\...
probe18_repeat2=debug\...
```

Er schreibt:

```text
dio_mini_family_maturation_path.csv
dio_mini_family_maturation_path_detail.csv
dio_mini_family_maturation_path.json
dio_mini_family_maturation_path.md
```

Er macht passiv sichtbar:

```text
conflict -> observed -> carried
conflict -> observed
observed -> carried
carried -> carried
observed -> observed
```

Probe18-Beispiel:

```text
dio_0t0v:
  conflict -> observed -> carried

dio_1vpi:
  conflict -> conflict -> observed

dio_14xc:
  observed -> observed -> observed

dio_0arw:
  carried -> carried -> carried

dio_1u7v:
  carried -> carried -> carried
```

Wichtig:

```text
Der Reifeverlauf ist keine Anweisung.
Er ist eine passive Chronik.

Er sagt:
  diese Familie hat sich ueber reale Begegnungen so entwickelt.

Er sagt nicht:
  naechstes Mal muss so gehandelt werden.
```

Wirkungsgrenze:

```text
Keine Motorik.
Kein Memory-Schreiben.
Kein Gate.
Keine harte Regel.
```

## Passive Konfliktspur-Lupe

Zweck:

```text
Wenn eine Familie negativen realen Kontakt hatte,
liest die Lupe passiv alle spaeteren und frueheren Kontakte dieser Familie.
```

Sie beantwortet:

```text
Wurde der Konflikt spaeter getragen?
Blieb der Konflikt nur Beobachtung?
Wurde der Konflikt weiter negativ wiederholt?
Welche Sensorlage lag dabei an?
```

Beispiel Probe17/18:

```text
dio_0t0v:
  negative Spur in probe18_first
  spaeter getragene positive Spur in probe18_repeat2
  passive_conflict_state=conflict_reorganized_to_carried

dio_1vpi:
  negative Spur in probe18_first und probe18_repeat1
  spaeter nur Beobachtung/Vorsicht
  passive_conflict_state=conflict_to_observation
```

Mechanische Grenze:

```text
Die Lupe darf nicht entscheiden.
Die Lupe darf nicht belohnen.
Die Lupe darf nicht bestrafen.
Die Lupe darf keine Schwelle setzen.

Sie ist eine passive Innenwahrnehmung:
  Das hat weh getan.
  Das wurde spaeter getragen.
  Das blieb vorsichtig.
```

Wichtig:

```text
Diese Lesart ist keine Strategy.
Sie ist eine Konfliktchronik zwischen realem Kontakt,
innerem Zustand und spaeterer Familienwirkung.
```

## Passive Konflikt-Innenwahrnehmung

Die Konfliktspur kann in eine lesbare Innenwahrnehmung uebersetzt werden:

```text
dio_0t0v:
  Diese Familie hatte Konflikt, wurde spaeter aber getragen.

dio_1vpi:
  Diese Familie blieb nach Konflikt vorsichtig/beobachtend.
```

Fachliche Bedeutung:

```text
DIO bekommt damit keine neue Regel.
DIO bekommt eine passive Lesbarkeit seiner eigenen Konfliktchronik.

Das entspricht:
  Diese Spur tat weh.
  Diese Spur wurde spaeter tragend.
  Diese Spur bleibt vorsichtig.
```

Grenze:

```text
Diese Innenwahrnehmung ist kein Entscheidungsanker.
Sie ist kein Trade-Signal.
Sie ist kein Memory-Update.
Sie ist kein Reife-Gate.

Sie kann spaeter als Grundlage fuer echte Innenreflexion dienen,
aber erst wenn die Speicherwirkung explizit gebaut wird.
```

## Passive Reflexionskandidaten

Aus der Konflikt-Innenwahrnehmung duerfen passive Reflexionskandidaten entstehen:

```text
dio_0t0v:
  reflection_candidate_reorganized_trace
  Was hat sich zwischen Konflikt und spaeterem Tragen geaendert?

dio_1vpi:
  reflection_candidate_cautious_trace
  Warum bleibt diese Spur nach Konflikt eher Beobachtung als getragener Kontakt?
```

Fachliche Grenze:

```text
Ein Reflexionskandidat ist eine Markierung fuer spaeteres Lesen.
Er ist keine Entscheidung.
Er ist keine Reife.
Er ist kein Vertrauen.
Er ist keine Vorsicht.
Er ist kein Schutzmechanismus.
```

Wichtig:

```text
Die Kandidaten duerfen erst dann Wirkung bekommen,
wenn ein separater Reflexionsspeicher ausdruecklich gebaut wird.

Bis dahin bleiben sie Diagnostik.
```

## Passive Reflexionskandidaten-Zeitlinie

Reflexionskandidaten koennen mit dem passiven Innenprotokoll verbunden werden:

```text
Kandidat -> Innenzustand ueber Ticks -> Kontaktverlauf -> passive Frage
```

Beispiel:

```text
dio_0t0v:
  inner_carried bleibt stabil.
  Kontaktverlauf geht von negativ ueber beobachtet zu positiv.
  Das ist eine reorganisierte Spur.

dio_1vpi:
  inner_cautious bleibt stabil.
  Kontaktverlauf geht von negativ zu Beobachtung.
  Das ist eine vorsichtige Spur.
```

Wichtig:

```text
Diese Zeitlinie zeigt Reifepotenzial,
aber sie ist noch keine Reife.

Sie zeigt Schutzdistanz,
aber sie ist noch kein Schutzmechanismus.

Sie zeigt getragenen Verlauf,
aber sie ist noch kein Vertrauensspeicher.
```

Grenze:

```text
Keine Wirkung auf Entry.
Keine Wirkung auf Motorik.
Keine Wirkung auf Memory.
Keine harte Regel.
```

## Passive Reflexionsreife

Aus der Kandidaten-Zeitlinie kann eine passive Reifelesung entstehen:

```text
reflection_reorganized_readable:
  Konflikt wurde spaeter getragen.

reflection_cautious_unresolved:
  Konflikt wurde beobachtet,
  aber noch nicht getragen.
```

Beispiel:

```text
dio_0t0v:
  reflection_reorganized_readable
  positive_contacts=4
  negative_contacts=1
  observed_contacts=2

dio_1vpi:
  reflection_cautious_unresolved
  positive_contacts=0
  negative_contacts=5
  observed_contacts=6
```

Wirkungsgrenze:

```text
Reflexionsreife ist hier nur Lesbarkeit.
Sie ist keine gespeicherte Reife.
Sie ist kein Vertrauen.
Sie ist kein Schutz.
Sie ist kein Handlungssignal.

Erst ein spaeter explizit gebauter Reflexionsspeicher duerfte daraus
eine echte innere Erfahrung machen.
```

## Reflexionsspeicher-Entwurf

Der Reflexionsspeicher ist als eigener Bauplan festgehalten:

```text
40_REFLEXIONSSPEICHER_ENTWURF.md
```

Vertrag:

```text
Memory bleibt reale Erfahrung.
Thought bleibt gedachte Moeglichkeit.
Reflexionsspeicher bleibt Innenlesart ueber reale Erfahrung.
```

Nicht erlaubt:

```text
Reflexion ersetzt reale Erfahrung.
Reflexion macht Thought zur Wahrheit.
Reflexion setzt Entry frei.
Reflexion blockiert Entry.
Reflexion erzeugt harte Reife.
```

Erlaubt als spaeterer Forschungsweg:

```text
Diese reale Kontaktgeschichte wurde innerlich so gelesen.
Diese Spur war Konflikt und wurde spaeter getragen.
Diese Spur blieb vorsichtig und ungeloest.
Diese Frage bleibt offen.
```

Damit ist die naechste Speicherstufe fachlich vorbereitet,
aber noch nicht aktiviert.

## Passive Reflexionsspeicher-Schema-Pruefung

Vor echtem Reflexionsspeicher-Schreiben prueft ein passiver Leser,
ob die Mindeststruktur vorhanden waere:

```text
DIO_MINI/report_passive_reflection_memory_schema_check.py
```

Probe17/18:

```text
dio_0t0v:
  schema_state=eligible_passive_schema
  real_contact_path=negative:1 -> observed:2 -> positive:4
  inner_state_path=carried:7
  writes_memory=0

dio_1vpi:
  schema_state=eligible_passive_schema
  real_contact_path=negative:5 -> observed:6
  inner_state_path=cautious:11
  writes_memory=0
```

Grenze:

```text
eligible_passive_schema bedeutet nur:
  spaeter speicherfaehig im Sinne des Schemas.

Es bedeutet nicht:
  aktiv gespeichert
  aktiv gelernt
  aktiv vertraut
  aktiv vorsichtig
  aktiv handlungsnah
```

## Passive Reflexionsschema-Stabilitaet

Ein weiterer passiver Leser kann mehrere Schema-Checks vergleichen:

```text
DIO_MINI/report_passive_reflection_schema_stability.py
```

Er darf nur feststellen:

```text
single_source_baseline
stable_passive_schema
schema_state_changed
reflection_maturity_changed
real_contact_path_changed
inner_state_path_changed
```

Probe17/18 hat aktuell nur eine Quelle:

```text
dio_0t0v:
  single_source_baseline

dio_1vpi:
  single_source_baseline
```

Grenze:

```text
Baseline bedeutet Vergleichspunkt.
Baseline bedeutet nicht Stabilitaetsbeweis.
Stabilitaet bedeutet spaeter nur passive Lesbarkeit.
Stabilitaet bedeutet nicht Handlung, Trust oder Schutz.
```

## Passive Reflexionsschema-Stabilitaet mit zwei Quellen

Vergleich:

```text
probe17_18
probe18_only
```

Befund:

```text
dio_0t0v:
  stable_passive_schema
  reflection_reorganized_readable

dio_1vpi:
  stable_passive_schema
  reflection_cautious_unresolved
```

Grenze:

```text
stable_passive_schema bedeutet:
  Die passive Lesart bleibt ueber die gelesenen Quellen gleich.

Es bedeutet nicht:
  speichern
  handeln
  vertrauen
  blockieren
  schuetzen
```

## Passive Reflexionsschema-Pipeline

Die Reflexionsschema-Kette darf automatisiert werden:

```text
DIO_MINI/run_passive_reflection_schema_pipeline.py
```

Aber:

```text
Automatisierung ist keine Aktivierung.
```

Der Runner darf nur Debug-/Diagnosedaten erzeugen.

Er darf nicht:

```text
Memory schreiben
Reflexionsspeicher schreiben
Entry beeinflussen
Trust erzeugen
Schutz erzeugen
Gates setzen
```

Korrektur:

```text
Numerische 0 ist ein gueltiger Wert.
0 darf nicht als fehlendes Feld gewertet werden.
```

## Probe19: ruhige Wiedererkennung ohne Reflexionsspeicher

Probe19 wurde als kontrollierter Folgelauf mit kopiertem Mini-Speicher gelesen:

```text
debug\dio_mini_probe19_followup_same_memory\
debug\dio_mini_passive_cortex_probe19_followup\
debug\dio_mini_passive_reflection_schema_pipeline_probe19_followup\
```

Passive Innenlage:

```text
inner_carried:
  dio_0arw,dio_0t0v,dio_1u7v

inner_open_observation:
  dio_14xc

inner_unfinished:
  dio_00qb,dio_1vpi
```

Schema-Befund:

```text
schema_rows=0
```

Grenze:

```text
Stabile Wiedererkennung ist noch kein Reflexionsspeicher.
Ruhiges Wiedersehen darf nicht automatisch speichern.

Speicherfaehig wird eine Spur erst, wenn sie passiv eine relevante
Differenz zeigt:
  Konflikt
  Reorganisation
  vorsichtige offene Spannung
  veraenderte reale Kontaktfolge
  veraenderte Innenlage
```

Damit bleibt die Wirkung organisch getrennt:

```text
Wiedererkennung:
  ich sehe/fuehle diese Familie wieder.

Reflexionsspeicher:
  hier gab es eine innere Differenz, die spaeter sinnvoll lesbar sein muss.
```

## Passiver Wiedererkennungsgrenzen-Bericht

Modul:

```text
DIO_MINI/report_passive_recognition_boundary.py
```

Aufgabe:

```text
Unterscheiden, ob eine gelesene Spur nur wiedererkannt wird
oder ob sie eine reflexionswuerdige Differenz enthaelt.
```

Zulaessige passive Zustände:

```text
stable_recognition_not_memory
open_observation_not_memory
unfinished_trace_not_memory
reflection_worthy_difference
undecided_passive_boundary
```

Grenze:

```text
Der Bericht schreibt kein Memory.
Der Bericht beeinflusst keine Handlung.
Der Bericht ist kein Gate.
Der Bericht ist keine Regel.
```

Validierung:

```text
Probe19:
  keine reflection_worthy_difference
  ruhige Wiedererkennung bleibt ohne Reflexionsspeicher.

Probe17/18:
  reflection_worthy_difference=6
  Differenzspuren werden passiv erkannt.
```

Wichtig:

```text
reflection_worthy_difference bedeutet:
  Diese Spur darf spaeter als Reflexionsspeicher-Kandidat betrachtet werden.

Es bedeutet nicht:
  sofort speichern
  sofort vertrauen
  sofort handeln
  sofort blockieren
```

## Passive Reifungsdruck-Karte

Modul:

```text
DIO_MINI/build_passive_maturity_pressure_map.py
```

Aufgabe:

```text
Aus einem passiven Innenwahrnehmungs-Runtime-Trace wird eine
Reifungsdruck-Karte gebildet.

Sie beschreibt, ob eine Familie wiederholt getragen gewirkt haette,
Mini-DIO aber trotzdem in WAIT geblieben ist.
```

Zustaende:

```text
passive_overcautious_carried_pressure
passive_cautious_potential_pressure
passive_action_withholding_split_pressure
passive_context_dependent_withholding_pressure
passive_open_potential_pressure
passive_action_trust_seed_pressure
passive_unloaded_no_inner_awareness
passive_unclassified_pressure
```

Wirkungsgrenze:

```text
Die Karte ist kein Entry-Signal.
Die Karte ist kein Gate.
Die Karte ist keine Motorik.
Die Karte schreibt kein Runtime-Memory.
Die Karte sagt nicht LONG oder SHORT.
```

Zulaessige Lesung:

```text
Diese Familie erzeugt passive Inneninformation.
Sie kann spaeter als Reflexionsspeicher-Kandidat geprueft werden.
```

Nicht zulaessige Lesung:

```text
Diese Familie muss handeln.
Diese Familie darf handeln.
Diese Familie hat genug Mut.
Diese Familie ist ein Trade-Setup.
```

Besondere Grenzen:

```text
passive_unloaded_no_inner_awareness:
  Es gibt noch keine geladene passive Innenlage.
  Keine Rueckfuehrung.
  Keine Speicherreifung.

passive_action_trust_seed_pressure:
  Es gibt eine passive Vertrauensspur.
  Diese ist noch kein Mutsignal und kein Entry.

passive_open_potential_pressure:
  Es gibt offene potenzielle Tragfaehigkeit.
  Offen bedeutet nicht frei handeln.
```

Warum diese Grenze wichtig ist:

```text
Mini-DIO soll keine mechanische Regel aus einer Diagnose ableiten.

Reifungsdruck ist eine innere Wahrnehmung:
  "Meine Zurueckhaltung und die spaetere Weltkonsequenz
   stehen in Spannung."

Erst wenn diese Spannung stabil,
mehrfach und kontextuebergreifend tragend bleibt,
darf sie in einen getrennten Reflexionsspeicher-Kandidaten wandern.
```

## Passive Reflexionsspeicher-Kandidaten

Modul:

```text
DIO_MINI/build_passive_reflection_memory_candidates.py
```

Aufgabe:

```text
Aus der passiven Reifungsdruck-Karte wird eine Kandidatenliste gebildet.

Kandidat bedeutet:
  Die Familie ist wiederholt genug,
  um spaeter als Reflexionsspeicher-Spur geprueft zu werden.
```

Zulaessige Kandidatenzustaende:

```text
candidate_stable_overcautious_reflection
candidate_stable_cautious_reflection
candidate_stable_trust_seed_reflection
candidate_stable_open_potential_reflection
candidate_context_dependent_reflection
candidate_action_withholding_split_reflection
```

Nicht-Kandidaten:

```text
not_candidate_unloaded_no_inner_awareness
not_candidate_single_world_only
not_candidate_unclassified
```

Wirkungsgrenze:

```text
Kandidat ist kein Reflexionsspeicher.
Kandidat ist kein Entry.
Kandidat ist kein Trust-Wert fuer Handlung.
Kandidat ist keine Regel.
Kandidat ist keine Motorik.
```

Gueltige Lesung:

```text
"Diese Familie darf spaeter tiefer reflektiv geprueft werden."
```

Ungueltige Lesung:

```text
"Diese Familie soll jetzt handeln."
"Diese Familie ist sicher."
"Diese Familie hebt Vorsicht auf."
```

## Passive Kandidatenvalidierung

Modul:

```text
DIO_MINI/validate_passive_reflection_candidates.py
```

Aufgabe:

```text
Kandidaten werden gegen held-out Welten geprueft,
die nicht zur Kandidatenbildung verwendet wurden.
```

Validierungszustaende:

```text
candidate_recurred_with_passive_withholding
candidate_recurred_without_withholding
candidate_seen_without_inner_awareness
candidate_not_seen_in_validation_world
not_validated_not_candidate
```

Wirkungsgrenze:

```text
Validiert bedeutet:
  Die Familie ist passiv wiedergekehrt
  und darf gesondert reflektiv untersucht werden.

Validiert bedeutet nicht:
  handeln
  Vertrauen freischalten
  Mut erhoehen
  Gate oeffnen
  Entry erzeugen
```

Spezialfall:

```text
candidate_recurred_with_passive_withholding

Lesung:
  Wiederkehrende Familie,
  weiterhin passiv zurueckgehalten,
  im Nachblick potenziell tragend.

Grenze:
  Das ist eine Reflexionslupe wert,
  aber noch keine Runtime-Wirkung.
```

## Passive Reflexionslupe

Modul:

```text
DIO_MINI/report_passive_reflection_candidate_lupe.py
```

Aufgabe:

```text
Eine einzelne validierte Kandidatenfamilie wird ueber Bildungswelten
und held-out Validierungswelten im Detail gelesen.
```

Wirkungsgrenze:

```text
Die Lupe ist kein Speicher.
Die Lupe ist kein Entry.
Die Lupe ist kein Gate.
Die Lupe ist keine Richtung.
```

Besonders wichtig:

```text
Wenn eine Familie im Nachblick sowohl LONG als auch SHORT tragen kann,
darf sie nicht als Richtungssignal gelesen werden.

Dann ist sie hoechstens eine wiederkehrende Innen-/Formlage,
die genauer untersucht werden muss.
```

Gueltige Frage:

```text
Was bleibt ueber Welten stabil?
  Sehen?
  Hoeren?
  Fuehlen?
  Innenlage?
  Nachblick?
```

Ungueltige Frage:

```text
Welche Richtung soll aus dieser Familie gehandelt werden?
```

## Passive Sinnes-/Innenlage-Trennung

Modul:

```text
DIO_MINI/report_passive_candidate_sense_separation.py
```

Aufgabe:

```text
Eine passive Kandidatenfamilie wird getrennt gelesen nach:
  Sehen
  Hoeren
  Fuehlen
  Reflexionskontext
  Nachblick-Richtung
```

Wirkungsgrenze:

```text
Stabiles Sehen ist kein Entry.
Stabiles Fuehlen ist kein Entry.
Stabile Innenlage ist kein Entry.
Variable Nachblick-Richtung sperrt jede Richtungsauslegung.
```

Zulaessige Lesung:

```text
"Diese Familie ist eine wiederkehrende Form-/Feldlage."
```

Ungueltige Lesung:

```text
"Diese Familie ist LONG."
"Diese Familie ist SHORT."
"Diese Familie darf handeln."
```

Beispiel dio_0x52:

```text
Sehen stabil.
MCM-Kohaerenz stabil.
Innenlage stabil uebervorsichtig.
Nachblick-Richtung variiert LONG/SHORT.

Folge:
  passive Reflexionsfamilie ja.
  Richtung nein.
  Entry nein.
```

## Passive Reflexionsnotiz

Modul:

```text
DIO_MINI/build_passive_reflection_note.py
```

Aufgabe:

```text
Aus einer Sinnes-/Innenlage-Trennung wird eine passive Notiz erzeugt.

Die Notiz ist ein klares Artefakt:
  Was wurde stabil gesehen/gefuehlt?
  Was war variabel?
  Darf daraus Richtung entstehen?
```

Wirkungsgrenze:

```text
passive_only: true
writes_runtime_memory: false
read_by_mini_dio: false
influences_action: false
is_gate: false
is_motoric: false
is_entry_signal: false
is_direction_signal: false
```

## Praebewusste Aktivitaetsmuster

Einordnung:

```text
Praebewusste Aktivitaetsmuster liegen zwischen Wahrnehmung und bewusster
Deutung.
```

Sie entstehen aus:

```text
Sehen
Hoeren
Fuehlen
MCM-Feldwirkung
Nachhall
Memory-Naehe
Fragmentwiederkehr
```

Sie sind noch nicht:

```text
Strategie
Hypothese als Wahrheit
Handlung
Richtung
Entry
Gate
```

Gueltige Speicherlesung:

```text
Diese Fragmentstruktur taucht wiederholt als innere Vorstruktur auf.
```

Ungueltige Speicherlesung:

```text
Diese Fragmentstruktur ist schon gereifte Erfahrung.
Diese Fragmentstruktur darf aktiv handeln.
```

Wirkungsgrenze:

```text
Praebewusste Muster duerfen in passiver Diagnose sichtbar werden.
Sie duerfen erst nach Realitaetsbindung, Konsequenz und Reifung
in aktive Erfahrung uebergehen.
```

## Passive Semantik-Kandidatenkarte

Diagnoseebene:

```text
passive_semantic_candidate_map
```

Aufgabe:

```text
Fragmentwiederkehr in passive Rollen einordnen.
```

Rollen:

```text
sensorisch_affektiver_kern
visueller_formanteil
affektive_feldwirkung
auditive_energie
reflektiver_kontextanteil
randspur_oder_rauschen
```

Aktueller Kern:

```text
fuehlen_mcm_coherence
sehen_form_stability
```

Aktueller Reflexionsanteil:

```text
reflection_context_alignment
reflection_context_carry
reflection_context_strain
```

Gueltige Lesung:

```text
DIO bildet eine passive Rollenkarte praebewusster Aktivitaetsmuster.
```

Ungueltige Lesung:

```text
Diese Karte ist schon aktive Sprache.
Diese Karte ist schon Strategie.
Diese Karte darf schon handeln.
```

Wirkungsgrenze:

```text
passive_only: true
writes_runtime_memory: false
read_by_mini_dio: false
influences_action: false
is_gate: false
is_motoric: false
is_entry_signal: false
is_direction_signal: false
```

## Passive Fragmentwiederkehr

Diagnoseebene:

```text
passive_fragment_recurrence
```

Aufgabe:

```text
Pruefen, ob einzelne Fragmente ueber mehrere passive Fragmentinseln
wiederkehren.
```

Aktueller Kern:

```text
fuehlen_mcm_coherence
sehen_form_stability
```

Aktuelle Ziel-Erweiterung:

```text
fuehlen_mcm_tension
hoeren_energy_tone
reflection_context_alignment
reflection_context_carry
reflection_context_strain
```

Gueltige Lesung:

```text
Dieses Fragment wiederholt sich in mehreren passiven Naehe-Kontexten.
```

Ungueltige Lesung:

```text
Dieses Fragment ist dadurch schon Handlung.
Dieses Fragment ist dadurch schon Richtung.
Dieses Fragment ist dadurch schon Handelsreife.
```

Wichtig:

```text
Passive Fragmentwiederkehr ist staerker als Einzelspur,
aber schwaecher als aktive Erfahrung.

Sie darf erst dann in eine aktive Schicht wandern,
wenn reale Konsequenz, Wiederkehr, Feldwirkung und DIOs Innenlage
getrennt bestaetigt wurden.
```

Wirkungsgrenze:

```text
passive_only: true
writes_runtime_memory: false
read_by_mini_dio: false
influences_action: false
is_gate: false
is_motoric: false
is_entry_signal: false
is_direction_signal: false
```

## Passive Fragmentinsel-Stabilitaet

Diagnoseebene:

```text
passive_fragment_island_stability
```

Aufgabe:

```text
Pruefen, ob Fragmentinseln ueber mehrere passive Staende stabil bleiben.
```

Aktuelle Grenze:

```text
single_passive_fragment_island_trace
```

Bedeutung:

```text
Eine Fragmentinsel wurde einmal sichtbar.
Das ist noch keine gereifte Semantik.
Das ist keine aktive Memory.
Das ist keine Handlungsnaehe.
```

Gueltige Lesung:

```text
Diese Insel ist ein beobachteter innerer Strukturkeim.
```

Ungueltige Lesung:

```text
Diese Insel ist stabil.
Diese Insel ist sicher.
Diese Insel darf handeln.
```

Wirkungsgrenze:

```text
passive_only: true
writes_runtime_memory: false
read_by_mini_dio: false
influences_action: false
is_gate: false
is_motoric: false
is_entry_signal: false
is_direction_signal: false
```

## Passive Fragmentinseln

Diagnoseebene:

```text
passive_fragment_island
```

Aufgabe:

```text
Fragmentgruppen aus einer Cluster-Drift-Lupe als eigene passive Inseln
sichtbar machen.
```

Beispiel:

```text
dio_0x52 + dio_0szn
```

Gemeinsame Kerninsel:

```text
dio_fragment_island_1k8xbbj
fuehlen_mcm_coherence
sehen_form_stability
```

Ziel-Erweiterungsinsel:

```text
dio_fragment_island_0sa325x
fuehlen_mcm_tension
hoeren_energy_tone
reflection_context_alignment
reflection_context_carry
reflection_context_strain
```

Gueltige Lesung:

```text
Ein Zeichen besitzt einen stabilen gemeinsamen Kern mit einem anderen Zeichen.
Ein Zeichen bildet zusaetzlich eigene Fragmente aus.
```

Ungueltige Lesung:

```text
Diese Fragmentinsel ist eine Strategie.
Diese Fragmentinsel ist eine Richtung.
Diese Fragmentinsel ist ein Entry.
```

Wirkungsgrenze:

```text
passive_only: true
writes_runtime_memory: false
read_by_mini_dio: false
influences_action: false
is_gate: false
is_motoric: false
is_entry_signal: false
is_direction_signal: false
```

## Passive Cluster-Drift-Lupe

Diagnoseebene:

```text
passive_cluster_drift_lupe
```

Aufgabe:

```text
Cluster nicht nur als Ganzes betrachten,
sondern in tragende und eigenstaendige Fragmente zerlegen.
```

Beispiel:

```text
dio_0x52 + dio_0szn
```

Gemeinsamer Kern:

```text
sehen_form_stability
fuehlen_mcm_coherence
```

Eigenfragmente von dio_0x52:

```text
fuehlen_mcm_tension
hoeren_energy_tone
reflection_context_alignment
reflection_context_carry
reflection_context_strain
```

Gueltige Lesung:

```text
Diese Zeichen finden als Ganzes Naehe.
Im Detail hat ein Zeichen neue eigene Fragmente aufgebaut.
```

Ungueltige Lesung:

```text
Diese Naehe ist ein Entry.
Diese Naehe ist Richtung.
Diese Naehe muss gehandelt werden.
```

Fachliche Bedeutung:

```text
Aus Emergenz kann Verdichtung entstehen.
Aus Verdichtung kann Fragmentierung sichtbar werden.
Aus Fragmentierung koennen spaeter neue Clusterinseln entstehen.

Dieser Schritt bleibt aber passiv,
bis reale Erfahrung, Konsequenz und Feldwirkung spaeter getrennt bestaetigen,
dass daraus eine tragende Handlung naeher ruecken darf.
```

Wirkungsgrenze:

```text
passive_only: true
writes_runtime_memory: false
read_by_mini_dio: false
influences_action: false
is_gate: false
is_motoric: false
is_entry_signal: false
is_direction_signal: false
```

## Passive Clusterkandidaten

Modul:

```text
DIO_MINI/report_passive_sign_cluster_candidates.py
```

Output:

```text
debug/dio_mini_passive_sign_cluster_candidates_dio_0x52_v1/
  passive_sign_cluster_candidates.csv
  passive_sign_cluster_candidates_summary.csv
  passive_sign_cluster_candidates.json
  passive_sign_cluster_candidates.md
```

Aktueller Befund:

```text
dio_cluster_18u8wxs:
  dio_0x52 + dio_0szn
  passive_cluster_candidate_mixed_field_relation
```

Fachliche Bedeutung:

```text
Zwei passive Zeichen bilden wiederkehrend Naehe.
Diese Naehe ist selbst benennbar.
```

Wirkungsgrenze:

```text
read_by_mini_dio: false
writes_runtime_memory: false
influences_action: false
is_gate: false
is_motoric: false
is_entry_signal: false
is_direction_signal: false
```

Wichtig:

```text
mixed_field_relation bedeutet:
  offen halten,
  weiter pruefen,
  nicht Richtung lesen.
```

## Passive Clusterstabilitaet

Modul:

```text
DIO_MINI/report_passive_sign_cluster_stability.py
```

Output:

```text
debug/dio_mini_passive_sign_cluster_stability_dio_0x52_v1/
```

Befund:

```text
dio_0x52 + dio_0szn:
  drifting_passive_cluster_candidate

dio_0x52 + dio_0eh8:
  recently_stable_passive_cluster_candidate

dio_0x52 + dio_0hd3:
  recently_stable_passive_cluster_candidate

dio_0x52 + dio_0qze:
  recently_stable_passive_cluster_candidate
```

Wichtige Grenze:

```text
Clusterstabilitaet ist keine Handlungsstabilitaet.
Clusterdrift ist keine Fehlfunktion.

Clusterdrift bedeutet:
  Die innere Beziehung zwischen Zeichen veraendert sich,
  waehrend die Zeichen selbst reifen oder ihre Signatur aendern.
```

Konsequenz fuer DIO_MINI:

```text
Cluster duerfen erst dann in eine passive Leseschicht,
wenn sie ueber weitere Proben stabil bleiben.
Aktuell bleibt alles Diagnose.
```

Gueltige Nutzung:

```text
Dokumentieren.
Spaeter pruefen.
Mit anderen passiven Notizen vergleichen.
```

Ungueltige Nutzung:

```text
Runtime lesen.
Entry ableiten.
Richtung ableiten.
Mut oder Vertrauen direkt erhoehen.
```

## Passive Reflexionsnotiz-Pipeline

Modul:

```text
DIO_MINI/run_passive_reflection_note_pipeline.py
```

Aufgabe:

```text
Mehrere passive Reflexionskandidaten automatisch durchlaufen:
  passive Lupe
  Sinnes-/Innenlage-Trennung
  passive Reflexionsnotiz
  Emergenz-Lesung
```

Aktueller Befund:

```text
dio_0x52:
  held-out wiedergekehrt
  stabile Form-/Feldlage
  stabile uebervorsichtige Innenlage
  variable Nachblick-Richtung
  staerkster aktueller Emergenz-Kandidat

dio_0cgn:
  Emergenz-Kandidat im Bildungsraum
  bisher nicht held-out wieder gesehen
  deshalb noch nicht validiert
```

Was hier als Emergenz-Kandidat gilt:

```text
Eine Familie entsteht wiederkehrend aus Kopplung von Sehen, Fuehlen,
Innenlage und Nachblick, ohne dass Richtung, Entry oder Strategie
hart programmiert wurden.

Die Form-/Feldlage bleibt erkennbar.
Die Richtung bleibt offen.
Das System haelt zurueck.
```

Wichtig:

```text
Das ist kein endgueltiger Emergenz-Beweis.
Es ist ein belastbarer passiver Emergenz-Kandidat.
```

Wirkungsgrenze:

```text
passive_only: true
writes_runtime_memory: false
read_by_mini_dio: false
influences_action: false
is_gate: false
is_motoric: false
is_entry_signal: false
is_direction_signal: false
```

Naechste Pruefung:

```text
Weitere held-out Welten.
Weitere kontrollierte Sensorvarianz.
Pruefen, ob dio_0x52 als Form-/Feldlage stabil bleibt
oder nur lokale Syntaxnaehe war.
```

## Erweiterte held-out Pruefung probe7/probe8/probe9

Artefakte:

```text
debug/dio_mini_passive_reflection_candidate_validation_probe7_9
debug/dio_mini_passive_reflection_note_pipeline_validated_probe7_9
```

Befund:

```text
candidate_recurred_with_passive_withholding:
  families=4

stable_form_field_direction_candidate:
  dio_0eh8
  dio_0qze
  dio_0szn

emergence_candidate_form_field_without_direction:
  dio_0x52
```

Fachliche Grenze:

```text
stable_form_field_direction_candidate bedeutet:
  passive stabile Naehe von Form, Feld und Nachblick-Richtung.
  Noch keine Handlung.
  Noch keine Strategie.

emergence_candidate_form_field_without_direction bedeutet:
  passive stabile Form-/Feldlage,
  aber keine stabile Richtung.
  Genau diese Trennung ist fuer MCM wichtig,
  weil sie Form-/Feldwiederkehr ohne mechanische Richtungsregel zeigt.
```

Besonders wichtig:

```text
dio_0x52 darf weiterhin nicht als Richtung gelesen werden.
Gerade weil LONG und SHORT im Nachblick variieren,
ist es kein Entry-Signal, sondern ein Kandidat fuer eine
emergente Form-/Feldlage.
```

## Probe20: Richtungsvarianz ohne Motorik

Probe:

```text
data/kontrolliert_sensor_relation_probe20_emergenz_richtungsvarianz_2episoden_5m_SOLUSDT.csv
```

Ziel:

```text
Form-/Feldnaehe erhalten,
Fortsetzung variieren,
Richtung nicht vorgeben,
Motorik nicht aktivieren.
```

Befund:

```text
Trades: 0

Validiert:
  dio_0x52

Kategorie:
  emergence_candidate_form_field_without_direction

Stabile Schichten:
  sehen_form_stability
  fuehlen_mcm_coherence

Variable Schicht:
  Nachblick-Richtung LONG|SHORT
```

Wirkungsgrenze:

```text
Auch dieser Befund bleibt passiv.
Er darf nicht in choose_action,
nicht in Entry,
nicht in Mut,
nicht in Vertrauen
und nicht in ein Gate zurueckgeschrieben werden.
```

Erlaubte Nutzung:

```text
Nur als Bauplan-/Diagnosebeleg:
Mini-DIO kann eine wiederkehrende Form-/Feldlage bilden,
die nicht auf eine feste Richtung reduziert werden darf.
```

## Probe21: Hoervarianz ohne Motorik

Probe:

```text
data/kontrolliert_sensor_relation_probe21_emergenz_hoervarianz_2episoden_5m_SOLUSDT.csv
```

Ziel:

```text
Formverwandtschaft beibehalten,
aber Range-/Volumenstruktur veraendern.

Damit wird die Hoeren-/Energieachse anders stimuliert,
ohne daraus eine neue Handlung zu bauen.
```

Befund:

```text
Trades: 0

Validiert:
  dio_0x52

Kategorie:
  emergence_candidate_form_field_without_direction

Stabile Schichten:
  sehen_form_stability
  fuehlen_mcm_coherence

Variable Schicht:
  Nachblick-Richtung LONG|SHORT
```

Wirkungsgrenze:

```text
Auch bei Hoervarianz bleibt dio_0x52 passiv.
Die Familie ist keine Trade-Freigabe.
Sie ist ein Diagnosebeleg fuer wiederkehrende Form-/Feldlage
unter veraenderter sensorischer Energie.
```

## Konsolidierte passive Emergenz-Evidenz

Modul:

```text
DIO_MINI/report_passive_emergence_evidence.py
```

Aufgabe:

```text
Mehrere passive Validierungen zusammenfuehren.
Nicht einzelne Laeufe ueberinterpretieren.
Evidenz pro Familie sichtbar machen.
```

Aktueller Befund:

```text
dio_0x52:
  evidence_state=repeated_passive_emergence_candidate
  validation_sources_seen=probe10_11|probe20|probe21|probe7_9
  validation_observation_count=12
  validation_withheld_best_trade_count=12
  validation_best_actions=LONG|SHORT
  stable_fields=fuehlen_mcm_coherence|sehen_form_stability
```

Abgrenzung:

```text
dio_0eh8
dio_0qze
dio_0szn

Diese Familien sind passive stabile Form-/Feld-/Richtungskandidaten.
Das ist nicht dasselbe wie dio_0x52.
```

Fachliche Grenze:

```text
repeated_passive_emergence_candidate bedeutet:
  wiederholte passive Form-/Feldlage,
  keine stabile Richtung,
  keine motorische Freigabe,
  keine harte Regel.

Das ist eine Evidenzkarte,
kein aktiver Speicher.
```

## Passive Sign Memory

Modul:

```text
DIO_MINI/build_passive_sign_memory.py
```

Speicher:

```text
bot_memory/dio_mini_passive_sign_memory.json
```

Aufgabe:

```text
Wiederkehrende passive Familien werden als eigene Zeichen verdichtet.
Das ist eine temporaer-semantische Ebene.
Sie wirkt wie eine unterbewusste Wiedererkennungskarte:
  Diese Lage kenne ich.
  Diese Lage kommt wieder.
  Diese Lage hat noch keine gereifte Richtung.
```

Aktueller Befund:

```text
dio_0x52:
  passive_sign_symbol=dio_sign_0w10iws
  sign_kind=recurrent_form_field_sign
  sign_state=known_lage_direction_unripe
  validation_source_count=4
  validation_observation_count=12
  stable_fields=fuehlen_mcm_coherence|sehen_form_stability
  validation_best_actions=LONG|SHORT
```

DIO-Satz:

```text
Ich kenne diese Lage als wiederkehrende Form-/Feldnaehe,
aber Richtung ist nicht gereift.
```

Grenze:

```text
passive_only: true
writes_runtime_memory: false
read_by_mini_dio: false
influences_action: false
is_gate: false
is_motoric: false
is_entry_signal: false
is_direction_signal: false
```

Wichtig:

```text
Diese Schicht darf nicht in choose_action gelesen werden.
Sie ist Beobachtungsuebernahme, keine Handlung.

Erst wenn Zeichen ueber weitere Welten stabil bleiben,
darf spaeter eine eigene passive Reflexionslesung daraus entstehen.
```

## Stabilitaet der Zeichen-ID

Wichtige Regel:

```text
Ein passives Zeichen darf nicht umbenannt werden,
nur weil mehr Beobachtungen oder mehr Validierungsquellen hinzukommen.
```

Deshalb gilt fuer `passive_sign_symbol`:

```text
Identitaetsbildend:
  symbol_family
  sign_kind
  sign_state
  stable_fields
  direction_state
  emergence_readings

Nicht identitaetsbildend:
  validation_source_count
  validation_observation_count
  validation_withheld_best_trade_count
```

Begruendung:

```text
Der Name ist das wiedererkannte Zeichen.
Die Zaehler sind Reifung/Zustand dieses Zeichens.
```

Aktueller Stand nach Probe22:

```text
dio_0x52:
  passive_sign_symbol=dio_sign_0wd2qf8
  validation_source_count=5
  validation_observation_count=14
  sign_state=known_lage_direction_unripe
```

## Passive Zeichenrelationen

Neue passive Auswertung:

```text
DIO_MINI/report_passive_sign_relations.py
```

Zweck:

```text
Passiv pruefen,
welche gespeicherten Zeichen einander nahe liegen.

Das ist eine Innenkarte.
Es ist kein Handlungssystem.
```

Beispielstand fuer `dio_0x52`:

```text
Naechster passiver Nachbar:
  dio_0szn
  relation_state=passive_sign_neighbor
  relation_score=0.562
  field_overlap=1.000
  action_overlap=0.500
  neighbor_state=known_lage_direction_candidate
```

Wichtige Grenze:

```text
Gleiche Feldnaehe bedeutet nicht gleiche Handlung.
Eine Zeichenrelation darf nicht automatisch in Richtung, Entry,
Motorik oder Gate uebersetzt werden.

Sie sagt nur:
  Diese Zeichen liegen in der inneren DIO-Syntax nahe beieinander.
```

Status:

```text
read_by_mini_dio: false
writes_runtime_memory: false
influences_action: false
is_gate: false
is_motoric: false
is_entry_signal: false
is_direction_signal: false
```

Fachliche Lesart:

```text
Das ist der Beginn einer temporaer-semantischen Innenkarte.
Wiederkehrende Zeichen koennen Nachbarschaften bilden,
ohne dass Mini-DIO daraus schon handeln muss.
```

## Passive Relationsstabilitaet

Neue Diagnose:

```text
DIO_MINI/report_passive_sign_relation_stability.py
```

Aufgabe:

```text
Mehrere passive Zeichenrelationskarten vergleichen.
Eine Relation gilt nicht dadurch als gereift,
dass sie einmal sichtbar wurde.

Erst Wiederkehr ueber mehrere Quellen macht sie diagnostisch belastbarer.
```

Aktueller Basisstand:

```text
debug/dio_mini_passive_sign_relation_stability_dio_0x52_v1/

relation_sources=1
relations=14
relation_stability_state=single_passive_relation
```

Wirkungsgrenze:

```text
single_passive_relation ist keine Reife.
single_passive_relation ist keine Strategie.
single_passive_relation ist keine Richtung.
single_passive_relation ist kein Entry.
single_passive_relation ist kein Gate.
```

Nutzung:

```text
Nur Diagnose.
Nur Bauplan.
Nur passive Innenkartenpruefung.
```

## Probe23 und stabile Nachbarschaft ohne Handlung

Probe23:

```text
Temporalvarianz.
dio_0x52 wurde nicht erneut gesehen.
Die Note-Pipeline blieb leer.
```

Damit gilt:

```text
Nicht-Sehen ist ebenfalls Information.
Ein Zeichen wird nicht reifer,
nur weil eine neue Probe existiert.
```

Aktueller Stand fuer `dio_0x52`:

```text
passive_sign_symbol=dio_sign_0wd2qf8
sign_state=known_lage_direction_unripe
validation_source_count=5
validation_observation_count=14
validation_sources_seen=probe10_11|probe20|probe21|probe22|probe7_9
```

Aktueller Relationsstand:

```text
dio_0szn:
  relation_stability_state=recurring_strong_passive_relation
  relation_source_count=2/2
  avg_relation_score=0.562
  avg_field_overlap=1.000
  avg_action_overlap=0.500
  related_sign_state=known_lage_direction_candidate
```

Wirkungsgrenze:

```text
recurring_strong_passive_relation bedeutet:
  stabile passive Naehe in der Innenkarte.

Es bedeutet nicht:
  gleiche Richtung,
  gleiche Handlung,
  Entry-Reife,
  Trade-Freigabe,
  Gate,
  Motorik.
```

Moegliche spaetere Nutzung:

```text
Eine passive Reflexionslesung darf spaeter sagen:
  "Diese Lage liegt nahe an einem gereifteren Nachbarzeichen."

Aber:
  Sie darf daraus nicht automatisch handeln.
  Sie darf nur Pruefnaehe, Wiedererkennung oder innere Orientierung liefern.
```

## Probe24: stabile passive Nachbarschaft 3/3

Probe24:

```text
Minimalsensorische Variante.
dio_0x52 wurde nicht erneut gesehen.
Die Note-Pipeline blieb leer.
```

Konsolidierte Zeichenlage:

```text
dio_0x52:
  passive_sign_symbol=dio_sign_0wd2qf8
  sign_state=known_lage_direction_unripe
  validation_source_count=5
  validation_observation_count=14

dio_0szn:
  passive_sign_symbol=dio_sign_02tz3f2
  sign_state=known_lage_direction_candidate
  validation_source_count=1
  validation_observation_count=4
```

Relationslage:

```text
dio_0x52 -> dio_0szn:
  relation_stability_state=recurring_strong_passive_relation
  relation_source_count=3/3
  avg_relation_score=0.562
  avg_field_overlap=1.000
  avg_action_overlap=0.500
```

Strenge Grenze:

```text
Auch 3/3 passive Relationsstabilitaet ist keine Handlung.

Erlaubt:
  passive Innenkarte
  passive Wiedererkennung
  passive Reflexionsnaehe
  passive Satzbildung

Nicht erlaubt:
  Entry
  Richtung
  Gate
  Motorik
  automatische Reifeuebernahme
```

Fachliche Formulierung:

```text
dio_0x52 kennt eine offene Form-/Feldlage.
dio_0szn liegt stabil in der Naehe und ist ein Richtungskandidat.

Mini-DIO darf daraus spaeter nur eine innere Pruefnaehe bilden,
keine automatische Handlung.
```

## Passive Reflexions-Satzschicht

Neue Diagnose:

```text
DIO_MINI/build_passive_sign_reflection_sentences.py
```

Ausgabe:

```text
debug/dio_mini_passive_sign_reflection_sentences_dio_0x52_v2/
```

Aufgabe:

```text
Passive Zeichenrelationen in lesbare DIO-Saetze verdichten.
Das ist eine Innenkarten-Sprache.
Es ist keine Handlungsschicht.
```

Aktueller Satzkern:

```text
dio_0x52:
Ich erkenne diese Lage als offen.
Sie liegt stabil nahe bei dio_0szn, einem Richtungskandidaten.
Ich pruefe weiter und handle daraus nicht automatisch.
```

Satzklassen:

```text
open_lage_near_direction_candidate:
  1

recurring_field_neighbor:
  3

recurring_loose_neighbor:
  11
```

Wirkungsgrenze:

```text
passive_only: true
writes_runtime_memory: false
read_by_mini_dio: false
influences_action: false
is_gate: false
is_motoric: false
is_entry_signal: false
is_direction_signal: false
```

Wichtige Unterscheidung:

```text
recurring_field_neighbor:
  wiederkehrende passive Naehe mit Feldueberlappung.

recurring_loose_neighbor:
  wiederkehrende Randnaehe ohne tragende Feldnaehe.
  Nicht ueberbewerten.
```

Naechste Grenze:

```text
Diese Saetze duerfen erst dann als passive Leseschicht geladen werden,
wenn ihre Symbole und Klassen ueber weitere Relationskarten stabil bleiben.
```

## Passive Satzstabilitaet

Neue Diagnose:

```text
DIO_MINI/report_passive_sign_sentence_stability.py
```

Ausgabe:

```text
debug/dio_mini_passive_sign_sentence_stability_dio_0x52_v1/
```

Befund:

```text
recently_stable_passive_sentence:
  14

changing_passive_sentence:
  1
```

Wichtigster Satz:

```text
dio_0x52 -> dio_0szn:
  latest_sentence_symbol=dio_reflect_1sbypka
  sentence_stability_state=recently_stable_passive_sentence
  kind_history=single_passive_neighbor|open_lage_near_direction_candidate|open_lage_near_direction_candidate
```

Wirkungsgrenze:

```text
recently_stable_passive_sentence bedeutet:
  Die letzten Satzstaende sind stabil.

Es bedeutet nicht:
  ausreichend fuer Runtime-Lesung,
  ausreichend fuer Handlung,
  ausreichend fuer Richtung,
  ausreichend fuer Entry.
```

Erlaubt:

```text
Dokumentation.
Diagnose.
Weitere Stabilitaetspruefung.
```

Noch nicht erlaubt:

```text
Mini-DIO liest diese Saetze aktiv.
Mini-DIO handelt aus diesen Saetzen.
Mini-DIO uebernimmt Richtung aus diesen Saetzen.
```

## Probe25: Zeichenverfeinerung statt Runtime-Reife

Probe25 hat `dio_0x52` erneut passiv sichtbar gemacht.

Wichtig:

```text
Das bestaetigt nicht automatisch die alte Satznaehe.
Es verfeinert die Zeichenidentitaet.
```

Vor Probe25:

```text
dio_0x52:
  passive_sign_symbol=dio_sign_0wd2qf8
  stable_fields=fuehlen_mcm_coherence|sehen_form_stability
```

Nach Probe25:

```text
dio_0x52:
  passive_sign_symbol=dio_sign_10ck4rn
  stable_fields=
    fuehlen_mcm_coherence
    fuehlen_mcm_tension
    hoeren_energy_tone
    reflection_context_alignment
    reflection_context_carry
    reflection_context_strain
    sehen_form_stability
```

Lesung:

```text
Gleiche Familie.
Andere passive Signatur.

Das ist Zeichen-Drift oder Zeichen-Reifung,
nicht Handlung.
```

Die Relation zu `dio_0szn` bleibt wiederkehrend,
aber nicht mehr stark und eindeutig:

```text
dio_0x52 -> dio_0szn:
  recurring_mixed_passive_relation
  relation_source_count=4/4
  avg_field_overlap=0.821429
```

Die Satzstabilitaet zeigt deshalb:

```text
changing_passive_sentence
```

Wirkungsgrenze:

```text
Solange ein Satz driftet,
darf er nicht als passive Runtime-Leseschicht geladen werden.

Auch ein wiederkehrendes Zeichen bleibt Diagnose,
solange seine Signatur sich noch verfeinert.
```

Naechste notwendige Diagnose:

```text
Passive Sign-Drift-Analyse:
  gleicher Familienname
  verschiedene passive Zeichen
  veraenderte stabile Sinnes-/Innenfelder
  keine Runtime-Wirkung
```

## Passive Sign-Drift-Analyse

Modul:

```text
DIO_MINI/report_passive_sign_identity_drift.py
```

Aufgabe:

```text
Passive Zeichen-Memory-Staende vergleichen.

Die Analyse unterscheidet:
  mehr Evidenz fuer dasselbe Zeichen
  andere Zeichen-ID bei gleicher Familie
  echte innere Signaturveraenderung
```

Identitaetsbildend bleiben:

```text
symbol_family
sign_kind
sign_state
stable_fields
direction_state
emergence_readings
```

Nicht identitaetsbildend:

```text
validation_source_count
validation_observation_count
validation_withheld_best_trade_count
```

Aktueller Befund:

```text
dio_0x52:
  identity_drift_state=passive_sign_identity_drift
  unique_passive_sign_symbols=3
  latest_passive_sign_symbol=dio_sign_10ck4rn
```

Probe26-Nachtrag:

```text
dio_0x52 wurde in Probe26 nicht erneut gesehen.
Die passive Signatur blieb trotzdem bei dio_sign_10ck4rn,
weil keine neue Evidenz hinzukam, die eine Ruecksetzung oder neue Signatur
rechtfertigt.
```

Wichtig:

```text
Nicht-Sehen ist keine Gegenbestaetigung.
Nicht-Sehen ist aber auch keine Reife.

Die Memory darf daraus nicht lernen:
  "Ich bin sicherer."

Sie darf nur festhalten:
  "Diese Welt hat das Zeichen nicht aufgerufen."
```

## Passive Emergenzcluster

Naechste moegliche Speicherebene:

```text
passive_sign_cluster
```

Aufgabe:

```text
Nicht nur einzelne Zeichen speichern,
sondern wiederkehrende Naehe zwischen Zeichen sichtbar machen.
```

Beispiel:

```text
dio_sign_A
dio_sign_B
treten ueber mehrere Proben in Naehe auf
-> passive Clusternaehe
-> moegliches Clusterzeichen
```

Wirkungsgrenze:

```text
Ein Clusterzeichen ist keine Handlung.
Ein Clusterzeichen ist keine Richtung.
Ein Clusterzeichen ist kein Entry.
Ein Clusterzeichen ist kein Gate.
```

Gueltige Lesung:

```text
Diese inneren Zeichen bilden wiederkehrend Beziehung.
```

Ungueltige Lesung:

```text
Diese Beziehung soll gehandelt werden.
```

Damit bleibt die Realitaetstrennung sauber:

```text
Zeichen beschreibt Innenlage.
Cluster beschreibt Beziehung zwischen Innenlagen.
Handlung entsteht erst spaeter aus gereifter Realitaetsbindung,
nicht aus der blossen Existenz eines Clusters.
```

Fachliche Grenze:

```text
Passive Sign-Drift ist keine Instabilitaet der Handlung.
Es ist eine Diagnose der inneren Zeichenbildung.

Sie bedeutet:
  Die gleiche Familie wurde wiedererkannt,
  aber ihre innere Signatur hat sich durch neue stabile Felder veraendert.
```

Wirkungsgrenze:

```text
passive_only: true
writes_runtime_memory: false
read_by_mini_dio: false
influences_action: false
is_gate: false
is_motoric: false
is_entry_signal: false
is_direction_signal: false
```
