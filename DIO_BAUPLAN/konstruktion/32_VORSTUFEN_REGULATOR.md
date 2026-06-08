# Vorstufen-Regulator

## Grundsatz

Ein Sinneswert ist noch keine MCM-Feldlage.

Zwischen Sinnesorgan und MCM-Feld liegt ein Vorstufen-Regulator. Dieser
entscheidet nicht hart, sondern uebersetzt die Wirkung eines Reizes auf das
innere Feld.

```text
Welt
  -> Sinnesorgan
  -> Vorstufen-Regulator
  -> MCM-Feld
  -> Regulation
  -> Handlung
```

## Sinneswerte

Sinneswerte behalten ihre eigene Skala:

- Sehen:
  - `coherence`: `-1 .. +1`
  - `visual_clarity`: `0 .. 1`
  - `visual_object_stability`: `0 .. 1`
  - `structure_quality`: `0 .. 1`
- Hoeren:
  - `frequency_hz`: technischer Frequenzbereich
  - `loudness`: normalisierte Lautheit
  - `compression`: `0 .. 1`
- Denken:
  - Hypothesen, Reife, Vertrauen, Zweifel

Diese Werte duerfen nicht direkt als MCM-Feld interpretiert werden.

## MCM-Feldwirkung

Das MCM-Feld arbeitet als innerer Spannungsraum:

```text
-3 .. 0 .. +3
```

In das Feld gelangt nur reflektierte Wirkung:

- Auslenkung
- Spannung
- Naehe / Distanz
- Kontaktstaerke
- Resonanz
- Ueberkopplung
- Nachhall
- Rueckfuehrungsdruck
- Tragfaehigkeit

## Aufgabe des Vorstufen-Regulators

Der Vorstufen-Regulator beantwortet:

- Wie stark trifft mich dieser Reiz?
- Bleibt er aeussere Wahrnehmung oder wird er innere Lage?
- Ist der Kontakt nah, fern, unscharf, ueberkoppelt oder tragend?
- Entsteht nur Aufmerksamkeit oder echte Feldauslenkung?
- Muss die Wirkung gedaempft, gehalten oder naeher betrachtet werden?

Beispiel:

```text
coherence = +0.70
visual_clarity = 0.60
contact_weight = 0.40

-> sichtbarer Aufwaertsreiz
-> aber nur mittlerer Kontakt
-> MCM-Wirkung bleibt begrenzt
```

Nicht:

```text
coherence +0.70 = MCM +2.10
```

Sondern:

```text
visual_direction = coherence
visual_strength = abs(coherence)
mcm_reflective_displacement =
    visual_direction
    * visual_strength
    * contact_weight
    * coupling_capacity
    * 3.0
```

## Technische Regel

Direkte Kopplungen sind fachlich falsch:

```text
coherence -> mcm_axis
frequency_hz -> mcm_axis
visual_form_label -> field_bearing
hypothesis -> field_reality
entry_intent -> field_support
```

Erlaubt ist:

```text
sensor_value
  -> sensory_contact_strength
  -> mcm_coupling_strength
  -> mcm_reflective_displacement
  -> mcm_reflective_tension
```

## Erste Umsetzung

Die Vorstufe ist jetzt als eigenes Modul angelegt:

```text
core/mcm_preregulator.py
```

Aktiver Zufluss:

```text
Sehen  -> mcm_preregulator -> MCM-Feldwirkung
Hoeren -> mcm_preregulator -> MCM-Feldwirkung
Memory -> mcm_preregulator -> MCM-Feldwirkung
Thought -> mcm_preregulator -> MCM-Feldwirkung
Outcome -> mcm_preregulator -> MCM-Feldwirkung
```

Der Regulator gibt keine Rohdaten weiter, sondern nur normierte Feldwirkungen:

- `mcm_reflective_bearing`
- `mcm_reflective_pressure`
- `mcm_reflective_coupling_load`
- `mcm_reflective_displacement`
- `mcm_reflective_field_position`
- `mcm_reflective_tension`
- `mcm_reflective_state`

`core/felt_state.py` trennt jetzt Roh-Sehen und reflektive Felt-Wirkung:

- `visual_coherence` bleibt Roh-Sehen.
- `visual_mcm_contact_weight` beschreibt, wie nah die sichtbare Form das
  innere Feld beruehrt.
- `visual_reflective_coherence` ist die vorregulierte Kohaerenz, die in
  `felt_risk`, `felt_opportunity`, `felt_stability`, `felt_alignment`,
  `external_pressure` und `uncertainty_pressure` eingehen darf.

Damit sieht DIO eine Form nicht automatisch als innere MCM-Lage. Erst der
Kontakt zur Form bestimmt, wie stark die sichtbare Kohaerenz als Felt-Wirkung
ankommt.

Die gleiche Trennung wird in `core/decision_regulation.py` weitergefuehrt:
Regulation und Thought duerfen Roh-Sehen kennen, aber fuer Reife,
Vor-Handlungsnaehe und Ereignisstaerke wird die reflektive Kohaerenz
verwendet.

`core/neurochemistry.py` bekommt die gleiche Vorstufenwirkung als organische
Modulation. Neurochemie ist dabei nicht Rohzufluss in das MCM-Feld, sondern
eine zweite organische Reglerebene: sie liest Druck, Tragfaehigkeit,
Kopplungslast und Spannung und moduliert daraus Aktivierung, Hemmung,
Stabilitaet, Stress und Rueckfuehrungsdruck.

Wichtig:

```text
MCM-Vorstufen-Regulator = Normierung von Sinn, Memory, Thought, Outcome
Neurochemischer Regulator = organische Modulation dieser Feldwirkung
MCM-Feld = Organ, das nur normierte Wirkung empfaengt
```

## Ziel

DIO soll nicht von jedem Sinnesreiz direkt innerlich verschoben werden. Er soll
sehen, hoeren und denken koennen, ohne dass alles sofort sein MCM-Feld
ueberflutet.

Das ist keine Handlungssperre. Es ist eine organische Reizuebersetzung.
