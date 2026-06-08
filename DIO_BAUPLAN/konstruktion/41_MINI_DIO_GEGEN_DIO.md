# 41 Mini-DIO gegen DIO

Ziel dieses Dokuments ist ein sauberer Abgleich zwischen dem aktuellen
Mini-DIO und dem grossen DIO. Mini-DIO ist nicht als kleiner Ersatz fuer DIO
gedacht, sondern als kontrollierter Testorganismus: weniger Schichten, weniger
Nebengeraeusch, klarere Beobachtung, ob MCM-Lernen wirklich traegt.

Der grosse DIO enthaelt bereits viele Organe. Das Problem war nicht fehlende
Tiefe, sondern Ueberkopplung: Sehen, Fuehlen, Denken, Hypothese, Regulation,
Entry und Debug wurden teilweise zu eng miteinander verwoben. Mini-DIO trennt
diese Ebenen wieder.

## Kurzfazit

Mini-DIO ist aktuell in diesen Punkten sauberer als der grosse DIO:

- klare Trennung zwischen Wahrnehmung, Handlung und Konsequenz
- eigene Syntax ueber Form-/MCM-Verdichtung
- Beobachtung kann lernen, ohne direkt Handlung zu werden
- positive Konsequenz baut Trust auf
- negative Konsequenz baut Caution auf
- positive Muster werden nicht blind in Konfliktwelten uebertragen

Mini-DIO ist aktuell noch flacher als der grosse DIO in diesen Punkten:

- Zeitwahrnehmung und Raumzeit-Tiefe
- Weltbewegungs-Nachhall
- Doppler-/Vorhall-Achse
- selektive visuelle Aufmerksamkeit
- multisensorische Bereichswahrnehmung
- neurochemische Innenlage
- aktives MCM-Feld als raeumliches Organ

Wichtig: Diese fehlenden Punkte sollen nicht mechanisch zurueckkopiert werden.
Sie muessen als kleine, passive und pruefbare Mini-Mechaniken entstehen.

## Gegenueberstellung

| Bereich | Grosser DIO | Mini-DIO aktuell | Bewertung | Naechster sauberer Schritt |
| --- | --- | --- | --- | --- |
| Welt | Backtest-/Live-Welt, mehrere Laufpfade, Order-/Positionslogik | kontrollierte CSV-Welt, kompakter Lauf | Mini ist sauberer testbar | vorerst so lassen |
| Sehen | `visual_perception`, `visual_cortex`, `visual_attention`, Formachsen, Objektnaehe | `form_flow`, `form_stability`, `form_change` | Mini sieht einfacher, aber stabiler | Form-Persistenz und Objektnaehe spaeter minimal ergaenzen |
| Hoeren | `market_audio`, Melody, Frequenz, Lautheit, Kompression, WAV-Debug | `energy_tone`, `energy_shift` | Mini hoert nur abstrakt, nicht tonal tief | Energie-Nachhall statt schweres Audio-Protokoll |
| Fuehlen / MCM | MCM-Feld, Kontaktlagen, Feldspannung, Raumzeitkontakt, Vorstufen-Regulator | `mcm_coherence`, `mcm_tension`, `mcm_asymmetry` + 12 Mini-Neuronen | Mini fuehlt klar, aber raeumlich flach | kleiner MCM-Vorstufen-Regulator, keine volle Felduebernahme |
| MCM-Neuron | viele Feld-, Kontakt- und Neurochemie-Einfluesse | einfache Neuronen mit Gewichtung, Aktivierung und Afterimage | Mini ist nachvollziehbar | Neuron nicht aufblasen, erst Zeit-/Nachhall ergaenzen |
| Memory | Weltmemory, Formsymbol-Memory, Thought-Memory, viele Familien | `SemanticMemory` mit Symbolen, Familien, Action-Stats, Observations, Trust/Caution | Mini ist wesentlich sauberer | Memory weiterhin getrennt halten: Handlung != Beobachtung |
| Thought | Hypothesen, Possibility Field, Thought Memory, Reflexion | aktive Hypothese entfernt; passive Reports vorhanden | Mini ist bewusst entlastet | Thought nur als passive Innenkarte, nicht als Entry-Anker |
| Regulation | grosse Meta-Regulation, Neurochemie, Distance, Courage, Reife, Schutz | organischer Action-Pressure, Trade-Caution, Observation-Reife | Mini ist kleiner, aber weniger neurochemisch | neurochemischen Spiegel passiv einfuehren |
| Handlung | Trade Plan, Entry-Preise, Gates, Exit, Orderlogik | WAIT/LONG/SHORT mit lokalem TP/SL-Konsequenzleser | Mini ist fuer Lernen ausreichend | keine Strategy-Labels einfuehren |
| Konsequenz | Outcome-Stimulus, Formsymbol-Entwicklung, Positionserlebnis | TP/SL/TIMEOUT/BOTH_TOUCHED -> Reward -> Trust/Caution | Mini beweist Lernrichtung gut | Konsequenz weiter als Hauptlehrer nutzen |
| Debug | viele Protokolle, teils Ueberlappung | passive Einzelreports | Mini ist uebersichtlicher | Reportmenge begrenzen, Kern nicht belasten |

## Was Mini-DIO bereits nachgewiesen hat

### 1. Beobachten ist nicht Handeln

Mini-DIO kann eine wiederkehrende Struktur wahrnehmen und unter `observations`
ablegen, ohne direkten Action-Trust zu erhoehen. Das ist wichtig, weil sonst
jeder Gedanke zu schnell Realitaet wird.

Nachgewiesene Kette:

```text
Form/MCM-Kontakt sichtbar
-> DIO handelt nicht
-> Beobachtung wird gelernt
-> Familie wird vertrauter
-> spaeter kann Handlung naeher ruecken
```

### 2. Positive Beobachtung kann spaeter Handlung tragen

In den kontrollierten Folgelaeufen entstand aus Beobachtung spaeter reales
Handeln:

```text
Observation -> Reife -> Handlung -> TP -> Trust
```

Das ist fachlich wichtiger als reine Trade-Anzahl. Es zeigt, dass Mini-DIO
nicht nur reagiert, sondern eine wiederkehrende Lage in Handlungssicherheit
ueberfuehren kann.

### 3. Negative Konsequenz erzeugt Distanz

Die negative Konsequenzkette funktioniert:

```text
Handlung -> SL -> Caution -> Distanz/WAIT
```

Das ist kein hartes Gate. Es ist eine gelernte Handlungsdistanz.

### 4. Positive Praegung wird nicht blind uebertragen

Der Gegenlauf auf einem Konfliktdatensatz zeigte keine stumpfe Uebertragung
positiver Familien. Mini-DIO blieb dort bei Beobachtung. Das ist ein gutes
Zeichen fuer Kontextbindung.

## Was dem Mini-DIO noch fehlt

### 1. Tiefe Zeitwahrnehmung

Der grosse DIO besitzt bereits eine tiefe Zeit-/Raumzeit-Schicht:

```text
temporal_identity
temporal_recurrence
temporal_afterimage
temporal_context_depth
mcm_spacetime_depth
spacetime_memory_bearing
spacetime_future_bearing
spacetime_reflection_need
spacetime_regulation_support
```

Mini-DIO hat dagegen nur Laufindex, Kerzenindex, Horizon und Familienwiederkehr.
Das reicht fuer episodisches Lernen, aber nicht fuer echte Tiefe.

Minimaler Mini-Ausbau:

```text
mini_temporal_identity
mini_family_age
mini_ticks_since_family_seen
mini_afterimage
mini_recurrence_strength
mini_time_distance
mini_temporal_trust_support
mini_temporal_caution_support
```

Diese Werte duerfen nicht direkt traden. Sie sollen nur anzeigen, ob eine
Familie zeitlich wiederkehrt, reift, verblasst oder fremd bleibt.

### 2. Weltbewegungs-Nachhall

Der grosse DIO besitzt `world_motion_afterimage` und Doppler-Achsen. Das ist
die technische Naehe zu dem Gedanken:

```text
Die Welt zieht weiter.
Im Inneren bleibt ein Nachbild.
Aus der Verschiebung entsteht ein Vorhall moeglicher Fortsetzung.
```

Mini-DIO hat ein Neuronen-Afterimage, aber noch keinen Weltbewegungs-Nachhall.
Das ist ein fehlender Kernpunkt.

Minimaler Mini-Ausbau:

```text
mini_world_afterimage
mini_motion_bias
mini_motion_shift
mini_doppler_hint
```

Auch hier gilt: kein Entry-Signal. Erst Wahrnehmung, dann Lernen.

### 3. Selektives Sehen

Der grosse DIO hat visuelle Aufmerksamkeit und Objektbildung. Mini-DIO sieht
nur einfache Formachsen. Das ist gut fuer Kontrolle, aber begrenzt.

Mini-DIO braucht spaeter nicht sofort den ganzen visuellen Kortex. Sinnvoller
ist eine kleine Stabilitaetsfrage:

```text
Ich sehe eine Form.
Bleibt sie ueber Zeit erkennbar?
Zerfaellt sie sofort?
Kommt sie wieder?
Hat sie Kontaktnaehe?
```

### 4. Neurochemischer Spiegel

Der grosse DIO hat Dopamin, Cortisol, Serotonin, Noradrenalin, GABA,
Acetylcholin, Endorphin und Glutamat als diagnostische/regulative Lage.
Mini-DIO hat bisher nur Trust/Caution/Readiness.

Mini-DIO sollte nicht direkt die volle Neurochemie bekommen. Sinnvoll ist
zuerst ein passiver Spiegel:

```text
trust_tone        -> positive Tragspur
caution_tone      -> Schutzspannung
strain_tone       -> Ueberlastungsnaehe
focus_tone        -> klare Wahrnehmungsnaehe
relief_tone       -> Entlastung nach tragender Konsequenz
```

Das ist noch keine neue Entscheidungsschicht. Es ist Innenwahrnehmung.

### 5. MCM-Feld als raeumliches Organ

Mini-DIO hat 12 MCM-Neuronen mit Aktivierung und Afterimage. Das ist ein guter
Start, aber noch kein raeumliches Feld mit Inseln, Kontaktzonen und lokaler
Ausbreitung.

Naechste Stufe waere nicht "mehr Werte", sondern Feldorganisation:

```text
welche Neuronen tragen aehnliche Spannung?
welche Aktivitaetsinsel bleibt?
welche Insel kippt?
welche Insel beruhigt sich nach Konsequenz?
```

## Was nicht aus dem grossen DIO zurueckgeholt werden soll

Diese Bereiche bleiben vorerst bewusst draussen:

- aktive Hypothese als Entry-Anker
- Strategy-Begriffe wie Pullback-System oder feste Entry-Muster
- harte innere Gates ausser oekonomische Mindestpruefung
- breite Thought-Memory-Kopplung in Handlung
- Debug-Protokolle, die den Kernlauf belasten
- starre Wenn-Dann-Handlung aus inneren Zustandswerten

Grund:

```text
Mini-DIO soll nicht intelligenter wirken, weil mehr Logik eingehakt wurde.
Mini-DIO soll reifer werden, weil Wahrnehmung, Konsequenz und Memory sauberer
zusammenfinden.
```

## Empfohlener naechster Schritt

Der naechste technische Schritt sollte die Mini-Zeitwahrnehmung sein.

Begruendung:

```text
Mini-DIO erkennt bereits Familien.
Mini-DIO lernt bereits Observation und Konsequenz.
Was fehlt, ist zeitliche Tiefe:
  War diese Familie gerade eben da?
  Kommt sie nach Abstand wieder?
  Ist sie noch Nachhall oder neue Realitaet?
  Wird sie vertrauter oder nur auswendig wiederholt?
```

Die Umsetzung soll klein bleiben:

```text
DIO_MINI/temporal_memory.py
DIO_MINI/report_temporal_family_trace.py
```

Zunaechst passiv:

- keine direkte Entry-Wirkung
- keine neue Hypothesenhandlung
- keine harte Reifeschwelle
- nur Beobachtung, Wiederkehr, Nachhall, Zeitdistanz

Erst wenn diese Spur ueber mehrere kontrollierte Laeufe stabil ist, darf sie
weich in Trust/Caution/Readiness zurueckwirken.

## Arbeitsregel fuer weitere Uebertragung

Alles, was aus dem grossen DIO nach Mini-DIO uebertragen wird, muss diese
Pruefung bestehen:

```text
1. Ist es Wahrnehmung, Memory, Regulation, Handlung oder Debug?
2. Ist es passiv beobachtbar, bevor es aktiv wirkt?
3. Vermischt es Gedanken mit Realitaet?
4. Entsteht daraus ein Gate oder eine weiche Erfahrungsspur?
5. Macht es Mini-DIO klarer oder nur groesser?
```

Wenn Punkt 3 oder 4 kritisch ist, wird die Mechanik nicht uebernommen.
