# DIO_MINI aktive Handlungsschicht

Diese Datei beschreibt, was im Mini-Kern aktuell wirklich Handlung steuert.

Wichtig:

```text
Kontaktlagen, Satzspuren, Konfliktlesung und Stabilitaetslesung sind passiv.
Die aktive Handlung sitzt aktuell in choose_action.
```

## Aktiver Pfad

Quelle:

```text
DIO_MINI\run_mini.py
choose_action
```

Aktiver Ablauf:

```text
build_senses
-> MiniMCMField.step
-> make_syntax_symbol / make_syntax_vector
-> memory.action_diagnostics
-> choose_action
-> evaluate_future
-> evaluate_trade_event
-> memory.learn / memory.learn_observation
-> field.learn
```

## Sensorische Grundlage

Quelle:

```text
DIO_MINI\mini_world.py
build_senses
```

Aktuelle Sinne:

```text
sehen:
  form_flow
  form_stability
  form_change

hoeren:
  energy_tone
  energy_shift

fuehlen:
  mcm_coherence
  mcm_tension
  mcm_asymmetry
```

Fachliche Lesart:

```text
Sehen beschreibt Formbewegung.
Hoeren beschreibt Marktenergie / Spannungswechsel.
Fuehlen beschreibt MCM-Lage.
```

## MCM-Neuronales Feld

Quelle:

```text
DIO_MINI\mcm_neuron.py
MiniMCMField
MCMNeuron
```

Das Feld liest die acht Sinneswerte:

```text
sehen.form_flow
sehen.form_stability
sehen.form_change
hoeren.energy_tone
hoeren.energy_shift
fuehlen.mcm_coherence
fuehlen.mcm_tension
fuehlen.mcm_asymmetry
```

Es erzeugt:

```text
activation
afterimage
signature
action_scores fuer WAIT, LONG, SHORT
```

Fachliche Lesart:

```text
Das Feld ist der aktuelle koerperliche Reiz-/Resonanzzustand.
Es ist noch kein Gedaechtnis.
```

## action_diagnostics

Quelle:

```text
DIO_MINI\semantic_memory.py
SemanticMemory.action_diagnostics
```

Gelesen werden:

```text
symbol_trust
symbol_caution
symbol_count
family_trust
family_caution
family_count
symbol_observation
family_observation
associative_raw
```

Erzeugt werden:

```text
symbol_bias
family_bias
observation_signal
observation_bias
observation_readiness
associative_bias
action_bias
readiness
```

Fachliche Lesart:

```text
symbol_trust / symbol_caution:
  konkrete Formwort-Erfahrung

family_trust / family_caution:
  verdichtete Familien-Erfahrung

observation_signal:
  erkannte, aber vorher nicht gehandelte Moeglichkeit

associative_raw:
  sensorische Naehe zu gespeicherten Familien
```

## choose_action

Quelle:

```text
DIO_MINI\run_mini.py
choose_action
```

Aktuell pro Aktion:

```text
base = action_scores[action]
bias = diagnostics[action].action_bias
wait_bias = kleine WAIT-Neigung, wenn Trade-Reife niedrig ist
trade_caution = Vorsicht bei unreifer Erinnerung oder schwachem Signal
score = base + bias + wait_bias - trade_caution
```

Danach:

```text
Aktion mit hoechstem score gewinnt.
```

## Was aktuell Handlung beeinflusst

Aktiv:

```text
aktueller Feldreiz:
  action_scores

direkte Erfahrung:
  symbol_trust
  symbol_caution

Familienerfahrung:
  family_trust
  family_caution

beobachtetes Lernen:
  observation_signal

sensorische Verwandtschaft:
  associative_raw

vorsichtige Reife:
  readiness
```

Passiv, nicht aktiv:

```text
contact_lagen
sentence_traces
sentence_conflicts
experience_landscape
stable_direction_traces
```

## Was organisch passt

Passend:

```text
Vertrauen steigt durch positive Handlungskonsequenz.
Vorsicht steigt durch negative Handlungskonsequenz.
Beobachten wird getrennt von Handeln gespeichert.
Familienerfahrung wirkt staerker als einzelnes Symbol.
Sensorische Verwandtschaft kann eine leichte Naehe erzeugen.
WAIT bleibt moeglich, wenn Handlung noch nicht reif genug ist.
```

Das passt zur Zielrichtung:

```text
Ein fuehlender Organismus lernt durch Handlung,
Konsequenz, Wiederkehr und vorsichtige Reifung.
```

## Mini-TP/SL-Konsequenzlesung

Quelle:

```text
DIO_MINI\mini_world.py
evaluate_trade_event
```

Mini-DIO nutzt nicht die grosse Order-/Trade-Stats-Engine.

Stattdessen gibt es eine kleine Konsequenzwahrnehmung:

```text
entry = aktueller Close
tp/sl Abstand = lokale aktuelle Kerzenreichweite
future window = kleiner Folgebereich
```

Moegliche Ereignisse:

```text
TP
SL
TIMEOUT
BOTH_TOUCHED
NO_TRADE
```

Fachliche Lesart:

```text
TP:
  Die Handlung wurde im kleinen Folgefenster getragen.

SL:
  Die Handlung hat Belastung erzeugt.

TIMEOUT:
  Die Handlung wurde weder klar getragen noch klar verletzt.

BOTH_TOUCHED:
  Die Kerze beruehrte TP und SL im selben Bereich.
  Ohne intrabar Reihenfolge wird das nicht als sicherer Sieg oder Verlust gelesen.

NO_TRADE:
  Keine reale Handlung, nur Wahrnehmung / Beobachtung.
```

Debug-Spalten in `episodes.csv`:

```text
outcome_event
event_reward
event_raw_return
tp_price
sl_price
exit_price
bars_held
close_reward
```

Abgrenzung:

```text
Das ist keine Strategie.
Das ist kein hartes Entry-System.
Das ist keine grosse Positionsverwaltung.

Es ist eine einfache Konsequenzlesung,
damit Mini-DIO echte TP/SL-nahe Rueckmeldung bekommt.
```

## Passiver Trade-Event-Bericht

Quelle:

```text
DIO_MINI\report_trade_events.py
```

Der Bericht liest nur `episodes.csv` und fasst zusammen:

```text
symbol_family
action
outcome_event
count
reward_sum
avg_reward
runs
ticks
```

Er darf nicht:

```text
Memory schreiben
Handlung beeinflussen
Reife erzeugen
Gates setzen
```

Zweck:

```text
TP- und SL-Familien schnell sichtbar machen,
ohne manuell CSV-Zeilen lesen zu muessen.
```

## Kritische Punkte

### 1. Feste Gewichtungen

Aktuell gibt es feste Gewichtungen:

```text
symbol_bias
family_bias
observation_signal
associative_bias
readiness
wait_bias
trade_caution
```

Fachliche Bewertung:

```text
Fuer den Mini-Kern als Testsystem ist das akzeptabel.
Fuer DIO als organisches System duerfen diese Werte spaeter nicht als
starre Regeln verstanden werden.
```

### 2. Beobachtungslernen wirkt bereits leicht aktiv

`observation_signal` fliesst in `action_bias` und `readiness`.

Fachliche Bewertung:

```text
Das ist vertretbar, weil Beobachtung nicht direkt handelt,
sondern nur eine leichte Naehe erzeugt.

Es muss aber klein bleiben.
Sonst wird "ich habe es beobachtet" zu "ich muss handeln".
```

### 3. Associative Raw

`associative_raw` liest sensorische Verwandtschaft aus Familienvektoren.

Fachliche Bewertung:

```text
Das ist die erste sehr einfache Form von Aehnlichkeitsdenken.
Es ist kein Satzgedaechtnis.
Es ist keine Hypothese.
Es ist nur sensorische Naehe.
```

### 4. Mini-Motorik ist noch sehr direkt

Die Aktion entsteht sofort aus Scorevergleich.

Fachliche Bewertung:

```text
Fuer DIO_MINI reicht das.
Fuer den grossen DIO braucht es spaeter eine Reflexionsschicht,
aber erst wenn der kleine Kern stabil verstanden ist.
```

## Aktuelle harte Grenze

Nicht einbauen:

```text
Kontaktlage direkt in choose_action.
Satzspur direkt in choose_action.
Stabile Richtung direkt als Entry.
Konfliktfamilie als hartes Block-Gate.
```

Erlaubt spaeter:

```text
Passive Reflexion:
  "Diese Familie ist widerspruechlich."
  "Diese Familie ist kontaktlagenuebergreifend bestaetigt."
  "Diese Familie ist nur lokal bestaetigt."

Aber erst nach einer bewusst getrennten Reflexionsschicht.
```

## Diagnosewerkzeug fuer Handlungstreiber

Umgesetzt:

```text
DIO_MINI\report_action_drivers.py
```

Neue Debugfelder in:

```text
DIO_MINI\run_mini.py
episodes.csv
```

Zusaetzlich sichtbar:

```text
base_score_wait
base_score_long
base_score_short
wait_bias
trade_caution_long
trade_caution_short
immature_memory_pressure_long
immature_memory_pressure_short
weak_signal_pressure_long
weak_signal_pressure_short
```

Testlauf:

```text
debug\dio_mini_probe12_action_driver_check
debug\dio_mini_action_driver_probe12_v2
```

Befund:

```text
SHORT / memory_bias:
  count: 2
  reward_sum: 2.110077

LONG / memory_bias:
  count: 1
  reward_sum: 1.264211

WAIT / wait_regulation:
  count: 2

WAIT / episode_binding_hold:
  count: 1
```

Deutung:

```text
Der Probe12-Check handelt nicht primaer aus rohem Feldimpuls.
Die ausgefuehrten Trades kommen aus Memory-Bias.

WAIT entsteht teils durch normale Warteneigung,
teils durch Episodenbindung:
Ein neuer Tradeimpuls wird gehalten,
weil die vorherige Episode noch aktiv ist.
```

Wichtige Korrektur:

```text
WAIT ist nicht immer gleich WAIT.

wait_regulation:
  DIO entscheidet sich wirklich fuer Warten.

episode_binding_hold:
  DIO hatte einen Tradeimpuls,
  aber die laufende Episode bindet ihn noch.
```

Mechanische Grenze:

```text
report_action_drivers ist Diagnose.
Keine Handlung wird dadurch veraendert.
```

Naechster Schritt:

```text
Episodenbindung fachlich pruefen:
Ist episode_binding_hold organisch richtig,
oder unterdrueckt es manchmal sinnvolle neue Kontakte?
```

## Diagnose der Episodenbindung

Umgesetzt:

```text
DIO_MINI\report_episode_binding.py
```

Ausgaben:

```text
debug\dio_mini_episode_binding_probe12_v3
debug\dio_mini_episode_binding_probe13_v3
```

Der Report trennt:

```text
executed_aligned:
  DIO handelte und die reale Trainingsrueckschau bestaetigt die Richtung.

observed_not_bound:
  DIO beobachtete, obwohl die Rueckschau eine moegliche Richtung zeigt.

held_useful_impulse:
  DIO hatte einen LONG/SHORT-Impuls,
  aber die laufende Episode hielt ihn zurueck.
  Die Rueckschau zeigt, dass dieser Impuls tragend gewesen waere.

quiet:
  Kein tragender Rueckschauhinweis.
```

Neue Kennzahlen:

```text
unrealized_best_reward_sum:
  nicht realisierte Rueckschau-Bestaetigung.

held_impulse_potential_sum:
  Anteil davon, der durch aktive Episodenbindung gehalten wurde.
```

Passive Qualitaetsnamen:

```text
episode_binding_protective:
  Bindung hielt einen falschen oder unreifen Impuls zurueck.

episode_binding_overholding:
  Bindung hielt einen Impuls zurueck,
  der in der Rueckschau tragend gewesen waere.

observation_potential:
  DIO beobachtete, obwohl die Rueckschau eine moegliche Richtung zeigt.

executed_contact_confirmed:
  DIO handelte und die reale Rueckschau bestaetigt diese Handlung.
```

Probe12:

```text
executed_aligned:
  count: 3
  reward_sum: 3.374288

held_useful_impulse:
  count: 1
  held_impulse_potential_sum: 0.615236

observed_not_bound:
  count: 2
  unrealized_best_reward_sum: 0.276355
```

Probe13:

```text
executed_aligned:
  count: 5
  reward_sum: 6.009556

held_useful_impulse:
  count: 2
  held_impulse_potential_sum: 1.530746

observed_not_bound:
  count: 43
  unrealized_best_reward_sum: 24.373861
```

Fachliche Deutung:

```text
Episodenbindung ist nicht falsch.
Sie verhindert, dass DIO jeden neuen Reiz sofort motorisch verfolgt.

Aber sie kann zu klebrig werden:
Ein kleiner Teil tragender Impulse wird gehalten,
obwohl die Rueckschau zeigt, dass sie nuetzlich gewesen waeren.
```

Wichtige Grenze:

```text
Diese Diagnose aendert keine Handlung.
Sie zeigt nur, ob die Bindung schuetzt oder neue Kontakte unterdrueckt.
```

Naechster Schritt:

```text
Nicht die Bindung hart entfernen.
Stattdessen eine organische Lesung bauen:

Wann ist Episodenbindung Schutz?
Wann ist sie Ueberbindung?
Wann ist Beobachtung echte Reife und wann verpasster Kontakt?
```

## Bindungsqualitaet ueber mehrere Laeufe

Umgesetzt:

```text
DIO_MINI\report_binding_quality_matrix.py
```

Ausgabe:

```text
debug\dio_mini_binding_quality_matrix_v1
```

Vergleich:

```text
Probe12:
  episodes: 6
  executed: 3 / 3.374288
  overheld: 1 / 0.615236
  observed: 2 / 0.276355
  note: mixed

Probe13:
  episodes: 52
  executed: 5 / 6.009556
  overheld: 2 / 1.530746
  observed: 43 / 24.373861
  note: large_observation_potential
```

Fachliche Deutung:

```text
Probe12:
  DIO_MINI handelt bestaetigt,
  haelt aber einen kleinen tragenden Impuls zurueck.

Probe13:
  DIO_MINI beobachtet sehr viel moegliche Tragfaehigkeit,
  setzt aber nur wenige Kontakte um.
```

Wichtig:

```text
Das ist kein Beweis fuer "mehr Trades".
Es zeigt nur:
Die innere Beobachtung sieht mehr Moeglichkeiten,
als die aktuelle Handlungsschicht ausfuehrt.
```

Naechste mechanische Lesung:

```text
Beobachtungspotential nach Familien lesen:
Welche Formfamilien werden oft als moeglich tragend gesehen,
aber nicht gehandelt?

Auch das bleibt Diagnose.
```

## Beobachtungspotential nach Formfamilien

Umgesetzt:

```text
DIO_MINI\report_observation_potential.py
```

Ausgaben:

```text
debug\dio_mini_observation_potential_probe12_v2
debug\dio_mini_observation_potential_probe13_v2
```

Probe13 Top-Spuren:

```text
dio_0hd3:
  observed_count: 2
  best_reward_sum: 2.918570
  dominant_best_action: SHORT
  executed_aligned_count: 2
  executed_aligned_reward: 2.918570
  state: observation_later_confirmed

dio_1wie:
  observed_count: 3
  best_reward_sum: 2.383974
  dominant_best_action: SHORT
  executed_aligned_count: 1
  executed_aligned_reward: 0.794658
  state: observation_later_confirmed

dio_0c6o:
  observed_count: 2
  best_reward_sum: 2.296328
  dominant_best_action: LONG
  executed_aligned_count: 2
  executed_aligned_reward: 2.296328
  state: observation_later_confirmed
```

Weitere reine Beobachtung:

```text
dio_1g18:
  observed_count: 3
  best_reward_sum: 2.390277
  state: observed_only

dio_0jco:
  observed_count: 3
  best_reward_sum: 2.201961
  state: observed_only
```

Befund:

```text
Beobachtung ist nicht leer.

Ein Teil der beobachteten Familien wird spaeter bestaetigt gehandelt.
Ein anderer Teil bleibt Beobachtung.
```

Fachliche Grenze:

```text
observation_later_confirmed ist keine Entry-Regel.

Es zeigt nur:
DIO_MINI kann eine Formfamilie erst beobachten
und spaeter in derselben Welt bestaetigt ausfuehren.
```

Naechster Schritt:

```text
Die zeitliche Reihenfolge dieser Familien lesen:

Wann erscheint eine Familie zuerst als Beobachtung?
Wann wird sie spaeter ausgefuehrt?
Wie lange dauert diese Reifung in Episodenschritten?
```

## Zeitliche Reifung von Beobachtung zu Handlung

Umgesetzt:

```text
DIO_MINI\report_observation_maturation_timing.py
```

Ausgaben:

```text
debug\dio_mini_observation_maturation_probe12_v1
debug\dio_mini_observation_maturation_probe13_v1
```

Probe13:

```text
families: 18
matured: 3
open: 15
```

Gereifte Familien:

```text
dio_0hd3:
  state: observation_matured_to_execution
  observation_count: 2
  execution_count: 2
  run_lag: 2
  tick_lag: 0

dio_1wie:
  state: observation_matured_to_execution
  observation_count: 3
  execution_count: 1
  run_lag: 3
  tick_lag: 0

dio_0c6o:
  state: observation_matured_to_execution
  observation_count: 2
  execution_count: 2
  run_lag: 2
  tick_lag: 0
```

Offene Beobachtungen:

```text
dio_1g18
dio_0jco
dio_0u1i
dio_15ms
dio_12jm
dio_1k8m
dio_14jl
```

Befund:

```text
DIO_MINI zeigt im kontrollierten Probe13-Lauf:

Eine Formfamilie kann erst beobachtet werden.
Nach weiteren Episoden kann sie bestaetigt gehandelt werden.
Andere Formfamilien bleiben offen.
```

Fachliche Grenze:

```text
Auch diese Reifelesung ist passiv.
Sie sagt nicht:
"handle diese Familie".

Sie sagt nur:
"diese Familie hat in dieser Welt eine Beobachtung-zu-Handlung-Spur gezeigt".
```

## Folgelauf mit gleicher Memory

Kontrollierter Folgelauf:

```text
data\kontrolliert_sensor_relation_probe13_short_reife_varianz_shift_2episoden_5m_SOLUSDT.csv
bot_memory\dio_mini_sensor_relation_probe5_variation_memory.json
debug\dio_mini_probe13_followup_same_memory_v1
```

Runs:

```text
RUN 129:
  trades: 3
  reward: 3.4021

RUN 130:
  trades: 3
  reward: 3.4042

RUN 131:
  trades: 3
  reward: 3.4042

RUN 132:
  trades: 3
  reward: 3.4042
```

Bindungsqualitaet:

```text
executed_aligned:
  count: 12
  reward_sum: 13.614731

held_useful_impulse:
  count: 7
  held_impulse_potential_sum: 4.220735

observed_not_bound:
  count: 5
  unrealized_best_reward_sum: 0.979167
```

Vorher gereifte Familien im Folgelauf:

```text
dio_0c6o:
  LONG
  executed_aligned: 4
  reward je Ausfuehrung: 1.148164

dio_0hd3:
  SHORT
  executed_aligned: 4
  reward je Ausfuehrung: 1.459285

dio_1wie:
  SHORT
  executed_aligned: 1
  reward: 0.794658
```

Befund:

```text
Die vorher beobachtend gereiften Familien wurden im Folgelauf
nicht vergessen und nicht beliebig umgedeutet.

Sie wurden erneut handlungsnah erkannt und bestaetigt ausgefuehrt.
```

Wichtige Grenze:

```text
Das bleibt weiterhin Erfahrungsauswertung.
Es ist noch keine aktive Reflexionsschicht.
```

Naechste Entscheidung:

```text
Eine passive Reflexionsschicht ist jetzt fachlich gerechtfertigt,
aber sie darf nur lesen:

"Diese Familie wurde beobachtet, spaeter bestaetigt,
und im Folgelauf erneut bestaetigt."

Sie darf noch nicht direkt in choose_action eingreifen.
```

## Passive Reflexionsschicht v1

Umgesetzt:

```text
DIO_MINI\build_passive_reflection_layer.py
```

Ausgabe:

```text
debug\dio_mini_passive_reflection_probe13_followup_v1
```

Funktion:

```text
Die Schicht liest nur Familien,
die drei Bedingungen erfuellen:

1. zuerst beobachtet,
2. spaeter bestaetigt gehandelt,
3. im Folgelauf erneut bestaetigt.
```

Erste Reflexionskeime:

```text
dio_0hd3:
  reflection_seed_reconfirmed
  followup_exec: 4
  followup_reward: 5.837140

dio_0c6o:
  reflection_seed_reconfirmed
  followup_exec: 4
  followup_reward: 4.592656

dio_1wie:
  reflection_seed_reconfirmed
  followup_exec: 1
  followup_reward: 0.794658
```

Fachliche Bedeutung:

```text
Das ist die erste passive Reflexionsform:

"Diese Formfamilie wurde nicht nur einmal gehandelt.
Sie wurde beobachtet, reifte zur Handlung
und wurde im Folgelauf wieder bestaetigt."
```

Grenze:

```text
Diese Reflexionsschicht ist keine Motorik.
Sie wird nicht von choose_action gelesen.
Sie ist eine Leseschicht fuer spaetere Selbstwahrnehmung.
```

## Reflexionskeime in Memory

Umgesetzt:

```text
DIO_MINI\store_reflection_seeds.py
DIO_MINI\report_reflection_seeds.py
```

Memory:

```text
bot_memory\dio_mini_sensor_relation_probe5_variation_memory.json
```

Gespeichert:

```text
reflection_seeds: 3
```

Ausgabe:

```text
debug\dio_mini_reflection_seed_memory_report_v1
```

Gespeicherte DIO-Syntax:

```text
dio_reflect_11nxj7w:
  family: dio_0hd3
  reflection_seed_reconfirmed
  followup_reward: 5.837140

dio_reflect_01hi6xw:
  family: dio_0c6o
  reflection_seed_reconfirmed
  followup_reward: 4.592656

dio_reflect_1bdledh:
  family: dio_1wie
  reflection_seed_reconfirmed
  followup_reward: 0.794658
```

Wirkungsgrenze:

```text
reflection_seeds werden nicht in action_diagnostics gelesen.
reflection_seeds werden nicht in choose_action gelesen.
Sie sind nur passive Selbstwahrnehmung ueber Reifung.
```

Passivitaetstest:

```text
debug\dio_mini_reflection_passivity_check
```

Ergebnis:

```text
mit reflection_seeds:
  RUN 133
  trades: 3
  reward: 3.4042

ohne reflection_seeds:
  RUN 133
  trades: 3
  reward: 3.4042

episodes.csv:
  identischer Hash
```

Befund:

```text
Die gespeicherten Reflexionskeime veraendern die Handlung nicht.
Damit ist die Schicht aktuell praktisch passiv.
```

## Reflexionskeime als Selbstwahrnehmung lesen

Umgesetzt:

```text
DIO_MINI\report_reflection_self_awareness.py
```

Ausgabe:

```text
debug\dio_mini_reflection_self_awareness_v1
```

Klassifikation:

```text
self_awareness_stable:
  Der Reflexionskeim wurde beobachtet,
  spaeter bestaetigt,
  im Folgelauf mehrfach bestaetigt
  und ohne neue Beobachtungs-/Ueberbindungsreste getragen.

self_awareness_tentative:
  Der Reflexionskeim wurde bestaetigt,
  aber noch schwach oder nur teilweise.

self_awareness_report_only:
  Der Reflexionskeim bleibt Bericht.
```

Befund:

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

Detail:

```text
dio_reflect_11nxj7w:
  family: dio_0hd3
  self_awareness_stable
  reason: reconfirmed_without_observation_residue

dio_reflect_01hi6xw:
  family: dio_0c6o
  self_awareness_stable
  reason: reconfirmed_without_observation_residue

dio_reflect_1bdledh:
  family: dio_1wie
  self_awareness_tentative
  reason: partly_reconfirmed_after_observation
```

Wirkungsgrenze:

```text
Auch self_awareness_stable ist kein Handlungssignal.
Es ist nur eine passive Lesung:
"Diese Erfahrung ist stabiler Teil meiner Selbstwahrnehmung."
```

## Transfer-Lesung ohne Motorik

Ergaenzung:

```text
DIO_MINI\report_self_awareness_transfer.py
```

Diese Lesung prueft nach einem neuen Probe-Lauf:

```text
Wurde eine stabile Selbstwahrnehmungsfamilie wieder gesehen?
Wurde sie ausgefuehrt?
Hat sie getragen?
Oder blieb sie in dieser Welt still?
```

Probe14:

```text
dio_0hd3 wurde wiedererkannt und positiv getragen.
dio_0c6o wurde nicht gesehen.
dio_1wie wurde nicht gesehen.
```

Motorische Grenze:

```text
transfer_reconfirmed_clean ist noch keine Handlungsfreigabe.
Es ist nur eine passive Bestaetigung, dass DIO eine alte Erfahrung
in einer leicht veraenderten Welt wiederfinden kann.
```

Damit bleibt die aktive Schicht sauber:

```text
Handlung entsteht weiterhin aus aktueller Sensorik,
eigener Formsprache,
MCM-Kontakt
und erlebter Konsequenz.

Nicht aus einem Reflexionsbericht.
```

## Reflexionskarte bleibt ausserhalb der Handlung

Ergaenzung:

```text
DIO_MINI\report_self_awareness_reflection_map.py
```

Die Reflexionskarte formuliert passive Lesesaetze:

```text
"Ich erkenne eine alte Spur wieder und der Kontakt traegt."
"Ich kenne diese Spur, aber diese Welt ruft sie gerade nicht auf."
"Ich sehe eine alte Spur, aber sie bleibt Beobachtung."
"Ich erkenne eine alte Spur, aber der aktuelle Kontakt traegt sie nicht."
```

Diese Saetze sind keine Strategie und kein Entry-System.

Sie beschreiben nur:

```text
Erinnerung trifft aktuelle Welt.
Aktuelle Welt bestaetigt, verschweigt oder widerspricht der Erinnerung.
```

Aktive Handlung darf daraus erst spaeter entstehen, wenn eine separate
Reflexionsschicht sauber definiert ist. Stand jetzt:

```text
keine Rueckfuehrung in choose_action
keine Rueckfuehrung in score_long / score_short
keine Rueckfuehrung in trade_readiness
```

Probe15 bestaetigt diese Grenze:

```text
dio_0c6o wurde nach stiller Probe14-Lesung wieder positiv erkannt.
Das geschah ohne neue Motorik aus der Reflexionskarte.
```

Aktive Handlung bleibt daher weiterhin:

```text
Mini-MCM-Feld -> action_scores
SemanticMemory.action_diagnostics
choose_action
Konsequenzlernen
```

Nicht:

```text
reflection_memory_reconfirmed -> trade
```

Probe16 bestaetigt auch die Konfliktgrenze:

```text
dio_0c6o wurde gesehen.
Die alte LONG-Naehe trug in dieser Welt zuerst nicht.
DIO wechselte spaeter durch Konsequenzlernen auf SHORT.
```

Wichtig:

```text
Der Wechsel entstand aus der aktiven Mini-Handlungsschicht,
nicht aus der Reflexionskarte.
```

Die Reflexionskarte darf deshalb weiterhin nur beschreiben:

```text
reflection_memory_conflict:
  bekannte Spur gesehen,
  aktuelle Konsequenz widerspricht alter Tragnaehe.
```

Keine direkte Ableitung:

```text
reflection_memory_conflict -> blockiere
reflection_memory_conflict -> drehe Richtung
reflection_memory_conflict -> erzwinge WAIT
```

## Gespeicherte Reflexionskarte bleibt passiv

Aktualisierung:

```text
reflection_maps sind jetzt in SemanticMemory speicherbar.
```

Aber:

```text
store_reflection_maps.py schreibt nur passive Snapshots.
choose_action liest diese Snapshots nicht.
action_diagnostics liest diese Snapshots nicht.
```

Damit gilt weiterhin:

```text
Aktive Handlung lernt aus:
  ausgefuehrter Handlung
  beobachteter Konsequenz
  Symbol-/Familienerfahrung

Passive Reflexion liest:
  Erinnerung still
  Erinnerung getragen
  Erinnerung im Konflikt
```

## Konsequenzwirkung im Speicher lesen

Ergaenzung:

```text
DIO_MINI\report_memory_consequence_effect.py
```

Diese Diagnose verbindet zwei Ebenen:

```text
1. Was ist real im Lauf passiert?
   TP, SL, TIMEOUT, NO_TRADE

2. Wie ist diese Folge im SemanticMemory sichtbar?
   trust
   caution
   reward_sum
   action_count
```

Wichtig:

```text
Das ist keine aktive Handlungsschicht.
Das ist die Lupe auf die bereits gespeicherte Wirkung.
```

Aktiver Pfad bleibt:

```text
sehen / hoeren / fuehlen
Mini-MCM-Feld
action_scores
SemanticMemory.action_diagnostics
choose_action
Konsequenzlernen
```

Passiver Lesepfad:

```text
episodes.csv
trade_events_summary.csv
memory.json
memory_consequence_effect.csv
```

Befund:

```text
TP-Familien zeigen sichtbares Vertrauen.
SL-Familien zeigen sichtbare Vorsicht.
Wenn alte positive Erfahrung vorhanden ist, bleibt SL zuerst Spannung,
nicht sofort dominante Ablehnung.
```

Das passt zur Mini-DIO-Zielrichtung:

```text
keine harte Sperre
keine mechanische Richtungsaenderung
Konsequenz als gespeicherte Feld- und Handlungserfahrung
```

## Passive Konsequenz-Innenlage

Ergaenzung:

```text
DIO_MINI\report_passive_consequence_inner_awareness.py
```

Diese Schicht macht aus gespeicherter Konsequenz eine innere Lesart:

```text
inner_consequence_carried:
  Handlung wurde getragen.
  Vertrauen ist sichtbar.

inner_consequence_burdened:
  Handlung hat belastet.
  Vorsicht dominiert.

inner_consequence_conflicted:
  Handlung hat belastet,
  aber alte positive Erfahrung ist noch wirksam.

inner_consequence_quiet:
  keine reale Handlung.
```

Wichtig fuer die aktive Handlungsschicht:

```text
Noch keine Rueckkopplung in choose_action.
Noch keine Rueckkopplung in action_scores.
Noch keine Rueckkopplung in readiness.
```

Warum:

```text
Innenwahrnehmung muss zuerst lesbar und stabil werden.
Erst danach darf sie vorsichtig als Selbstregulation wirken.
```

## Tick-Protokoll der Konsequenz-Innenlage

Ergaenzung:

```text
DIO_MINI\report_passive_consequence_inner_state_protocol.py
```

Diese Schicht verbindet:

```text
Episode / Tick
aktuelle Symbolfamilie
reale Handlung
TP/SL/NO_TRADE
gespeicherte Konsequenz-Innenlage
```

Beispielhafte Lesung:

```text
inner_consequence_carried + real_contact_carried
  DIO sieht eine Familie, die innen getragen ist,
  und der reale Kontakt wird wieder getragen.

inner_consequence_conflicted + real_contact_burdened
  DIO sieht eine Familie mit widerspruechlicher Innenlage,
  und der reale Kontakt belastet erneut.
```

Aktive Grenze bleibt:

```text
Dieses Protokoll ist noch keine Handlungssteuerung.
Es ist die lesbare Innenhistorie eines Laufs.
```

## Multisensorische Innenkarte bleibt passiv

Ergaenzung:

```text
DIO_MINI\report_multisensory_inner_map.py
```

Diese Schicht liest pro Tick:

```text
sehen_form_flow / sehen_form_stability
hoeren_energy_tone
fuehlen_mcm_coherence / fuehlen_mcm_tension
inner_consequence_state
contact_state
```

Sie verdichtet daraus:

```text
sight_state
hearing_state
feeling_state
binding_state
```

Aktive Grenze:

```text
binding_state darf noch nicht handeln.
binding_state darf noch nicht blockieren.
binding_state darf noch nicht Richtung erzwingen.
```

Warum:

```text
Die Karte soll zuerst zeigen, ob DIO seine Welt multisensorisch
ueberhaupt konsistent liest.

Erst wenn diese Lesung stabil ist, kann daraus vorsichtig
Selbstregulation entstehen.
```

## Stabilitaet ist noch keine Handlung

Ergaenzung:

```text
DIO_MINI\report_multisensory_stability.py
```

Diese Schicht prueft:

```text
Wird dieselbe Familie ueber Wiederholung aehnlich gesehen,
gehoert, gefuehlt und innen gelesen?
```

Wichtig fuer die aktive Handlung:

```text
stabil != trade
stabil != gut
stabil != Freigabe
```

Stabil kann bedeuten:

```text
stabil getragen
stabil beobachtet
stabil widerspruechlich
stabil belastet
```

Aktiv relevant darf spaeter nur die Kombination werden:

```text
Wiederkehr
Konsequenzrichtung
aktuelle MCM-Lage
aktueller Kontakt
sensorische Kopplung
```

Stand jetzt bleibt der Report passiv.

## Reifungskarte bleibt ausserhalb der Motorik

Ergaenzung:

```text
DIO_MINI\report_multisensory_maturation_map.py
```

Diese Schicht liest:

```text
stabile positive Wiederkehr
stabile negative/widerspruechliche Wiederkehr
ruhige Beobachtung
gemischte Wiederkehr
```

Aktiv wichtig:

```text
maturation_stable_carried ist noch kein Trade.
maturation_stable_conflicted_burden ist noch kein Block.
maturation_mixed_recurrence ist noch kein Replan.
```

Die Reifungskarte ist vorerst nur:

```text
eine Selbstwahrnehmung der gelernten Wiederkehr.
```

Spaetere aktive Nutzung darf nur entstehen, wenn:

```text
Wiederkehr,
Konsequenz,
aktuelle MCM-Lage,
aktueller Kontakt
und sensorische Kopplung
gemeinsam tragend lesbar sind.
```

## Reife-Timeline bleibt passiv

Ergaenzung:

```text
DIO_MINI\report_multisensory_maturation_timeline.py
```

Diese Schicht zeigt:

```text
Wann taucht eine Familie auf?
Bleibt sie ruhig?
Wird sie getragen?
Wird sie widerspruechlich belastet?
Veraendert sie ihren Momentzustand ueber Wiederholung?
```

Wichtig:

```text
Eine Timeline ist noch keine Strategie.
Sie zeigt nur Entwicklung.
```

Beispiel:

```text
moment_quiet_held -> moment_quiet_held -> moment_carried
```

Das bedeutet:

```text
Eine Familie wurde erst gehalten/beobachtet
und spaeter real getragen.
```

Das darf spaeter fuer Reifung relevant werden, aber noch nicht direkt fuer Entry.

## Entwicklungsdiagnose bleibt passiv

Ergaenzung:

```text
DIO_MINI\report_passive_development_diagnosis.py
```

Diese Schicht verdichtet die Reife-Timeline zu:

```text
stabil getragen
Beobachtung/Halten zu getragenem Kontakt
ruhige Beobachtung
wiederholte Belastung
gemischter Wechsel
```

Aktiv wichtig:

```text
development_stable_carried ist noch kein Entry.
development_observation_to_carried ist noch keine Strategie.
development_repeated_burden ist noch kein Block.
```

Warum:

```text
DIO soll zuerst lernen, seine Entwicklung zu lesen.
Handlung aus Entwicklung kommt erst spaeter,
wenn diese Innenwahrnehmung stabil genug dokumentiert ist.
```

## Passiver Diagnose-Runner fuer Konsequenz und Entwicklung

Ergaenzung:

```text
DIO_MINI\run_passive_consequence_diagnostics.py
```

Dieser Runner erzeugt die ganze passive Kette:

```text
Trade-Ereignisse
Speicherwirkung
Konsequenz-Innenlage
Tick-Protokoll
Multisensorische Innenkarte
Stabilitaet
Reifung
Timeline
Entwicklungsdiagnose
```

Aktive Grenze:

```text
Der Runner ist nicht Teil der Motorik.
Er ist nicht Teil von choose_action.
Er ist kein Gate.
Er schreibt kein Memory.
```

Fachliche Rolle:

```text
Er macht DIOs passive Selbstwahrnehmung reproduzierbar lesbar.
```

## Livecheck Probe18 bestaetigt passive Grenze

Der kontrollierte Folgelauf mit kopierter Memory:

```text
bot_memory\dio_mini_pipeline_livecheck_memory.json
```

zeigte:

```text
3 Folgelaeufe
je 4 Trades
je 4 TP
0 SL
```

Die passive Entwicklungsdiagnose erkannte danach:

```text
development_stable_carried:
  dio_02qu
  dio_0arw
  dio_1u7v
  dio_1vpi

development_quiet_observation:
  dio_14xc
```

Wichtig fuer die aktive Handlungsschicht:

```text
Auch stable_carried ist noch keine automatische Handlungserlaubnis.
Es ist eine passive Innenwahrnehmung von Reifung.
Die aktive Schicht darf diese Information spaeter lesen,
aber sie darf daraus nicht sofort ein mechanisches Wenn-Dann-System machen.
```

Fachliche Konsequenz:

```text
DIO darf Reife erkennen.
DIO darf wiederkehrendes getragenes Erleben bemerken.
DIO darf belastete Wiederholung bemerken.

Aber:
Die Handlung muss weiterhin aus gekoppelter Wahrnehmung entstehen:
Sehen, Hoeren, Fuehlen, MCM-Feld, Konsequenzgedaechtnis.
```
