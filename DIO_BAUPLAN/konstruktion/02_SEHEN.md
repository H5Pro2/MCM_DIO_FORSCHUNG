# 02 Sehen

## Verbindliche Sinnestrennung

```text
Sehen   = Form / Struktur
Fühlen  = MCM-Feldwirkung
Hören   = Energie / Frequenz / Marktspannung
Denken  = Hypothese / Verdichtung
Handeln = erst nach tragender Kopplung
```

Sehen und Hören sind Marktsinne. Sie erzeugen Wahrnehmung, aber keine Order.
Das MCM-Feld fühlt die Wirkung dieser Wahrnehmung. Thought bildet daraus
Hypothesen. Handlung entsteht erst nach tragender Kopplung mit
Realitätsprüfung.

## Aufgabe

Sehen übersetzt Welt in Sinneswahrnehmung.

Im DIO-Bauplan umfasst diese Schicht:

- visuelle Formwahrnehmung
- hörbare Marktmelodie

DIO soll nicht nur einzelne Kerzen fühlen, sondern Formzusammenhänge sehen:

- Richtung
- Verdichtung
- Bereich
- Wiederkehr
- Bruch
- Nähe
- Entfernung
- Zeitliche Tiefe

## Drei Kernkanäle

Die rohe Kerzenübersetzung darf nicht alles in eine einzige Feldlage drücken.
Für den Neuaufbau gilt:

```text
coherence = Fühlen / MCM-Lage
asymmetry = Wahrnehmen / positive oder negative Prägung
energy    = Hören / Kerzenspannung als Rohmaterial der Marktmelodie
```

`energy` beschreibt damit zuerst die Schwingung des Marktreizes. Eine laute
oder stark rauschende Kerze ist nicht automatisch innere Unruhe. Sie ist ein
Stimulus, den Sehen, MCM-Feld und Regulation erst einordnen müssen.

## Hören als eigene Wahrnehmung innerhalb der Sehen-Schicht

Das Hören soll nicht als Liste vieler Einzelwerte nach außen laufen. Intern
darf DIO Rohenergie, Normalisierung und Limiter berechnen. Nach außen entsteht
eine kompakte Wahrnehmungsstruktur:

```text
market_hearing_state
```

Diese Struktur fasst die Marktmelodie zusammen:

- `loudness`: wie laut der Markt relativ zu seiner eigenen Normalität wirkt
- `frequency_hz`: Übersetzung der Lautstärke in einen gemeinsamen Hörraum
- `compression`: wie stark der Sinnesfilter begrenzt
- `tone`: kurze DIO-Syntax für den gehörten Zustand

Damit kann SOL seine eigene Melodie behalten und BTC ebenfalls, ohne dass DIO
beide Märkte über rohe Amplituden verwechselt. Das Ziel ist Wahrnehmung, nicht
mehr Variablenlast.

## Wichtig

Sehen ist keine Handlung.

Sehen sagt:

```text
Da ist eine Form.
Da ist Bewegung.
Da ist ein Bereich.
Da wiederholt sich etwas.
```

Sehen sagt nicht:

```text
Trade jetzt.
```

## Ausgabe

Die Sehen-Schicht gibt eine Formspur und eine Hörspur aus:

- `form_id`
- `form_family`
- `direction_trace`
- `compression_trace`
- `area_trace`
- `recurrence_trace`
- `time_depth`
- `market_hearing_state`

Diese Werte sind Beschreibungen, keine Regeln.

## Sehen als eigener Sinnesraum

Analog zum Hoeren bekommt DIO eine kompakte Sehstruktur:

```text
visual_sight_state
```

Diese Struktur ist kein MCM-Feld und keine Handlung. Sie beschreibt nur, was
DIO visuell als Form wahrnimmt:

- `form_id`: verdichtete Formbezeichnung
- `form_family`: einfache Formfamilie, z.B. Flussform, Bruchform, Druckform
- `clarity`: wie klar die Form sichtbar ist
- `object_stability`: wie stabil die Form als Objekt zusammenhaelt
- `coherence`: visuelle Kohaerenz
- `direction_bias`: sichtbare Richtungspraegung
- `range_position`: Lage im sichtbaren Bereich
- `form_pressure`: sichtbarer Formdruck
- `form_resonance`: sichtbare Formresonanz
- `form_fragility`: sichtbare Bruechigkeit
- `depth`: visuelle Tiefe
- `contact_candidate`: ob die Form als moeglicher Kontakt wahrgenommen wird
- `background_load`: wie viel visuelles Hintergrundrauschen vorhanden ist
- `sight_label`: kurze DIO-Syntax fuer den Sehzustand

Damit gilt:

```text
visual_sight_state   = Sehen
market_hearing_state = Hoeren
MCM-Feld             = Fuehlen / Empfinden
```

Eine sichtbare Form darf das MCM-Feld nur ueber reflektive Kopplung beruehren.
Sie ersetzt das Feld nicht und sie erzeugt keine Order.

## Visueller Kortex

Aus dem reinen Sehen entsteht eine zweite visuelle Verarbeitungsschicht:

```text
visual_sight_state
-> visual_cortex_state
```

`visual_sight_state` sagt: Ich sehe eine Form.

`visual_cortex_state` sagt: Diese Form bildet ein visuelles Objekt oder eine
Beziehung.

Beispiele fuer visuelle Objekte:

- `trend_object`: gerichtete Bewegung
- `range_object`: begrenzter Bereich
- `contact_object`: sichtbarer Kontaktbereich
- `compression_object`: Verdichtung / Kompression
- `break_object`: Bruch / fragile Form

Der visuelle Kortex darf diese Objekte zusaetzlich in Beziehung und Verlauf
setzen:

- `visual_object_relation_state`: Lage und Kontaktnaehe eines visuellen Objekts
- `visual_object_lifecycle_state`: Entstehen, Stabilisierung, Kontakt,
  Zurueckweisung oder Aufloesung eines visuellen Objekts

Damit entsteht eine feinere Sicht:

```text
Ich sehe ein Objekt.
Es liegt oben, unten oder in der Mitte meines sichtbaren Raums.
Es ist fern, nahe, am Kontakt oder nur Hintergrund.
Es entsteht, stabilisiert sich, wird beruehrt, kippt oder loest sich auf.
```

Diese Begriffe sind keine Strategie. Sie sind visuelle Orientierung. Erst
Memory, MCM-Feld, Thought und Realitaetspruefung duerfen spaeter zeigen, ob
diese sichtbare Orientierung tragend wird.

Regulatorisch darf der visuelle Kortex nur als Wahrnehmungsqualitaet wirken:

```text
stabile Objektbindung -> bessere visuelle Erdung
Kontaktnaehe          -> klarerer sichtbarer Objektkontakt
Aufloesung/Kippen     -> mehr Pruefbedarf
```

Er darf weiterhin keine Order setzen und keine MCM-Tragfaehigkeit behaupten.
Die neue Bruecke heisst deshalb nicht Handlung, sondern:

```text
visual_cortex_grounding
```

Dieser Wert sagt nur, ob das gesehene Objekt als Sichtobjekt tragfaehiger
gebunden ist.

Auch diese Schicht ist keine Strategie. Sie sagt nicht, wo DIO handeln muss.
Sie liefert nur eine sauberere visuelle Welt:

```text
Ich sehe nicht nur Kerzen.
Ich sehe eine Form.
Ich erkenne darin ein moegliches Objekt.
Ich pruefe spaeter, wie sich dieses Objekt im MCM-Feld anfuehlt.
```

## Selektive visuelle Aufmerksamkeit

Sehen erzeugt zuerst Wahrnehmung, nicht Feldstress.

DIO darf viele Formen bemerken, aber nicht jede sichtbare Form darf sofort mit
voller Kraft in das MCM-Feld laufen. Deshalb liegt zwischen rohem Sehen und
gefuehltem Kontakt eine weiche Aufmerksamkeitsschicht:

```text
visual_form_state
-> visual_attention_state
-> gewichteter MCM-Kontakt
```

Wichtige Felder:

- `visual_form_contact`: wie deutlich eine Form als Kontakt erscheint
- `visual_inspection_pull`: wie stark die Form genauer betrachtet werden will
- `visual_attention_depth`: wie tief DIO gerade hinsieht
- `visual_background_filter`: wie stark Hintergrundformen gedaempft werden
- `visual_mcm_contact_weight`: wie viel der gesehenen Form in das MCM-Feld
  weitergegeben wird

Damit bleibt Sehen breit, aber das Feld wird nicht von jeder Kerze direkt
ueberflutet. Erst wenn eine Form Aufmerksamkeit, Kontakt oder Untersuchungszug
bekommt, wirkt sie staerker auf die innere Lage.

Fachlich bedeutet das:

```text
Ich sehe etwas.
Ich betrachte es naeher.
Erst dann spuere ich staerker, wie es in mir wirkt.
```

Das ist keine Handlungssperre. Es ist Wahrnehmungsordnung.
