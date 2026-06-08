# 08 Konsequenz

## Aufgabe

Konsequenz ist die Rückkopplung der Realität.

Im Trading:

- TP
- SL
- Cancel
- Timeout
- Beobachtung war richtig
- Beobachtung hätte Gewinn verpasst
- Handlung war tragend
- Handlung war belastend

## Wirkung

Konsequenz wirkt zurück auf:

- MCM-Feld
- Memory
- Thought-Memory
- Regulation
- Vertrauen
- Vorsicht
- Reorganisation

## Getrennte Rückführung

Konsequenz schreibt getrennt zurück:

```text
reale Erfahrung -> Memory
Gedankenbewertung -> Thought-Memory
innere Wirkung -> MCM-Feld
Umgang damit -> Regulation
```

Beispiel:

```text
Die reale Form führte zu TP.
Mein Gedanke dazu war richtig.
Die Handlung war tragfähig.
Das Feld bekommt Vertrauen und Entlastung.
```

Oder:

```text
Die reale Form führte zu SL.
Mein Gedanke dazu war falsch oder unreif.
Die Handlung war belastend.
Das Feld bekommt Vorsicht, Lernspannung und Reorganisation.
```

Die Konsequenz darf niemals nachträglich einen Gedanken als reale Wahrheit
fälschen. Sie bewertet nur, ob der Gedanke an der Realität getragen hat.

## Wichtig

DIO lernt nicht nur:

```text
Gewinn gut, Verlust schlecht.
```

DIO lernt:

```text
Hat meine Wahrnehmung getragen?
Hat mein Gedanke getragen?
Hat meine Handlung getragen?
War Nicht-Handlung richtig?
War die Lage reif genug?
```

## DIO_MINI: einfache TP/SL-Konsequenz

Mini-DIO nutzt eine kleine Konsequenzlesung:

```text
DIO_MINI\mini_world.py
evaluate_trade_event
```

Sie liest:

```text
TP
SL
TIMEOUT
BOTH_TOUCHED
NO_TRADE
```

Abgrenzung:

```text
Das ist keine grosse Order-Engine.
Das ist keine Strategy.
Das ist kein hartes Entry-System.
```

Funktion:

```text
Mini-DIO bekommt eine konkrete Folge seiner Handlung.
TP bedeutet: Handlung wurde getragen.
SL bedeutet: Handlung hat Belastung erzeugt.
TIMEOUT bedeutet: Handlung blieb unklar.
BOTH_TOUCHED bedeutet: Intrabar-Reihenfolge ist nicht sicher lesbar.
NO_TRADE bedeutet: keine reale Handlung.
```

Damit kann Mini-DIO Konsequenz einfacher lernen als nur ueber:

```text
Close spaeter hoeher oder niedriger.
```

## Konsequenz im Speicher sichtbar machen

Mini-DIO hat fuer die Auswertung eine passive Lupe:

```text
DIO_MINI\report_memory_consequence_effect.py
```

Sie liest:

```text
Trade-Ereignis:
  TP
  SL
  TIMEOUT
  NO_TRADE

Memory-Wirkung:
  trust
  caution
  reward_sum
  action_count
```

Damit wird unterscheidbar:

```text
Die Handlung endete in TP.
Die Familie hat dadurch Vertrauen aufgebaut.

Die Handlung endete in SL.
Die Familie hat dadurch Vorsicht aufgebaut.

Die Handlung war widerspruechlich.
Vertrauen und Vorsicht tragen gleichzeitig Spannung.
```

Wichtig:

```text
Diese Lupe schreibt nicht zurueck.
Sie bewertet nicht fuer DIO.
Sie zeigt nur, ob die reale Konsequenz im Speicher angekommen ist.
```

## Konsequenz als passive Innenlage

Naechste passive Leseschicht:

```text
DIO_MINI\report_passive_consequence_inner_awareness.py
```

Sie formuliert Konsequenz nicht nur als Zahl, sondern als Innenlage:

```text
getragen
belastet
widerspruechlich
unklar
ruhig beobachtet
```

Beispiele:

```text
TP + Vertrauen > Vorsicht:
  inner_consequence_carried

SL + Vorsicht dominant:
  inner_consequence_burdened

SL + Vorsicht sichtbar, aber alte positive Erfahrung bleibt staerker:
  inner_consequence_conflicted
```

Fachlich:

```text
Eine belastende Konsequenz muss nicht sofort Ablehnung bedeuten.
Sie kann auch Widerspruch bedeuten:
  Ein Teil der Erfahrung traegt.
  Ein Teil der Erfahrung war verletzt.
  Das Feld muss diese Spannung erst lesen lernen.
```
