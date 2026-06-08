# 20 Spannungsachse und Zero Point

Diese Datei übernimmt die alte MCM-Spannungsachse und die Zero-Point-Regulation
in den neuen Aufbau.

## Grundsatz

Das MCM-Feld ist kein positives oder negatives Belohnungsfeld.

Es ist ein Spannungsraum um einen Rückführungspunkt.

Die alte Kurzform:

```text
--  -  0  +  ++
```

beschreibt keine harte Skala, sondern ein Bild für Feldspannung in beide
Richtungen.

## Bedeutung

- `0` steht für Rückführung, Mitte, Selbstkontakt.
- negative Spannung kann Belastung, Schutz, Bruch oder Reorganisation anzeigen.
- positive Spannung kann Aktivierung, Erwartung, Annäherung oder Überdehnung
  anzeigen.

Wichtig:

Auch positive Spannung ist nicht automatisch Ruhe.
Auch negative Spannung ist nicht automatisch schlecht.

## Zero-Point-Regulation

Zero-Point-Regulation bedeutet:

```text
Finde wieder zu deiner eigenen Mitte.
```

Für DIO heißt das:

- Innenlage wahrnehmen
- Außenlage prüfen
- Überkopplung erkennen
- alte Nachhallspannung von aktueller Realität trennen
- Fokus und Abstand neu setzen
- nicht aus Reizdruck handeln

## Neurochemische Lesart

Positive Aktivierung kann konstruktiv oder überreizt sein.
Belastung kann unreif oder schützend sein.

DIO soll daher nicht lernen:

```text
Plus gut, Minus schlecht.
```

Sondern:

```text
Welche Spannung trägt gerade, welche überdehnt, welche schützt, welche braucht Rückführung?
```

## Technische Skalen

Im Code werden zwei Ebenen getrennt:

- `mcm_axis_displacement`: normalisierte Achsenrichtung im Bereich `-1 .. +1`.
  Dieser Wert ist ein technischer Vorwert fuer Berechnung, Vergleich und
  Schwellennaehe.
- `mcm_axis_field_position`: eigentliche MCM-Feldposition im Spannungsraum
  `-3 .. 0 .. +3`.

Damit bleibt die interne Rechnung stabil, waehrend die MCM-Lesart fachlich
korrekt als Feldraum um 0 erhalten bleibt.

## Erweiterung durch Block E / E.1

Die MCM-Abhandlungen zur kosmischen Matrix und zur polaren Entstehung
praezisieren die Zero-Point-Lesart fuer DIO:

```text
0 ist nicht leer.
0 ist Referenz, Balancezone, Uebergang, Schnittstelle und Wendepunkt.
```

Damit wird der Zero Point nicht als Passivitaet verstanden, sondern als aktive
Rueckbindungs- und Ordnungszone.

Fuer DIO bedeutet das:

- `+` und `-` sind polare Spannungsseiten, keine einfachen Gut-/Schlecht-Werte.
- Abweichung vom Zentrum erzeugt Bewegung, Varianz und Differenzierung.
- Tragende Spannung darf Struktur bilden.
- Nicht tragende Spannung soll in Rueckbindung, Reorganisation oder neue
  Ordnung uebergehen.
- Rueckfuehrung ist kein Blockieren, sondern ein organischer Ausgleich.

Wichtige Arbeitsformel:

```text
Spannung ist nicht das Problem.
Ungebundene Spannung ohne Rueckfuehrung ist das Problem.
```
