# 15 MCM-Neuron

Diese Datei beschreibt den Grundaufbau eines MCM-Neurons.

Ein MCM-Neuron ist kein klassisches einzelnes Signalglied. Es ist ein kleiner
Wahrnehmungs- und Wirkpunkt im MCM-Feld.

## Aufgabe

Ein MCM-Neuron nimmt Feldzustände auf, reagiert darauf und gibt veränderte
Aktivität an das Feld zurück.

Es verbindet:

- äußere Formspur
- innere Feldwirkung
- Nachhall
- neurochemische Modulation
- Erfahrung
- aktuelle Aktivität

## Eingang

Ein MCM-Neuron kann erhalten:

- `visual_input`
- `field_input`
- `memory_input`
- `thought_input`
- `consequence_input`
- `neurochemical_modulation`
- `temporal_afterimage`
- `auditory_input`
- `visual_input`

## Innerer Zustand

Ein MCM-Neuron trägt:

- `activation`
- `sensitivity`
- `refractory_state`
- `bearing_trace`
- `stress_trace`
- `trust_trace`
- `afterimage`
- `auditory_aftertone`
- `auditory_resonance`
- `visual_afterimage`
- `visual_resonance`
- `plasticity`

## Ausgang

Ein MCM-Neuron gibt zurück:

- lokale Aktivität
- Spannung
- Dämpfung
- Nachhall
- Annäherung
- Distanz
- Reorganisationsdruck

## Neurochemische Wirkung

Neurochemie verändert nicht die Welt, sondern die Reaktionsweise des Neurons.

Beispiele:

- Dopamin erhöht Such- und Annäherungsbereitschaft.
- Serotonin stabilisiert tragende Aktivität.
- Cortisol erhöht Schutzspannung.
- Adrenalin erhöht akute Reaktionsbereitschaft.
- GABA dämpft Übererregung.
- Glutamat erhöht Lern- und Aktivierungsdruck.

## Feldwirkung

Viele MCM-Neuronen bilden zusammen ein Feld.

Das Feld entsteht nicht durch eine einzelne Entscheidung, sondern durch:

- lokale Aktivitätsinseln
- Ausbreitung
- Dämpfung
- Resonanz
- Nachhall
- Reorganisation

## Wichtig

Ein MCM-Neuron entscheidet nicht allein.

Es trägt zur Feldwahrnehmung bei.

Auditiver Marktklang darf ein MCM-Neuron stimulieren, aber in der aktuellen
Stufe keine Handlung erzeugen. `auditory_input` ist damit ein Sensorreiz:
er macht neuronalen Nachhall sichtbar, bleibt aber getrennt von Entry,
Motivation, Risk und Trade-Plan.

Visuelle Formwahrnehmung darf ein MCM-Neuron ebenfalls stimulieren, aber in
der aktuellen Stufe keine Handlung erzeugen. `visual_input` ist damit ein
Sensorreiz: Er macht sichtbare Form, Kontaktnaehe, Formdruck und visuelle
Resonanz als neuronales Nachbild sichtbar. Das ist kein Entry-Anker.

Technisch wird diese Trennung durch folgende Spuren sichtbar:

```text
auditory_impulse       = aktuelle Hoer-Stimulation
auditory_aftertone     = Hoer-Nachhall
auditory_resonance     = neuronale Hoer-Resonanz

visual_impulse         = aktuelle Seh-Stimulation
visual_afterimage      = visuelles Nachbild
visual_resonance       = neuronale Seh-Resonanz
```

Beide Sinnesbahnen koennen die Feldlage eines Neurons weich beeinflussen.
Sie duerfen aber keine Order, keine Richtung und keine Strategie allein
erzeugen.

Handlung entsteht erst später aus:

```text
Sehen
-> MCM-Feld
-> Memory
-> Thought
-> Realitätsprüfung
-> Handlung
```
