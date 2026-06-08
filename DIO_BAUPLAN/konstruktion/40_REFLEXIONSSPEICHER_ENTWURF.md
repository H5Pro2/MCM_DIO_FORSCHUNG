# 40 Reflexionsspeicher Entwurf

## Status

Dieser Entwurf ist passiv.

Er beschreibt, was ein spaeterer Reflexionsspeicher duerfte und was nicht.
Er ist noch kein aktiver Speicher, kein Gate, keine Motorik und keine
Handlungslogik.

## Zweck

Der Reflexionsspeicher soll spaeter DIOs Innenwahrnehmung ueber reale
Konflikt-, Beobachtungs- und Tragspuren lesbar halten.

Er speichert nicht:

```text
So ist die Welt.
```

Er speichert nur:

```text
So habe ich meine reale Erfahrung innerlich gelesen.
So hat sich diese Lesart spaeter veraendert.
```

## Strikte Realitaetstrennung

Die wichtigste Grenze:

```text
Reale Erfahrung bleibt Welt-Memory.
Gedanke bleibt Thought.
Reflexion bleibt Innenlesart ueber reale Erfahrung.
```

Der Reflexionsspeicher darf reale Erfahrung nicht ersetzen.

Er darf eine Hypothese nicht zur Realitaet machen.

Er darf eine passive Reifelesung nicht automatisch zu Vertrauen, Schutz oder
Entry-Naehe machen.

## Erlaubte Inhalte

Ein spaeterer Reflexionsspeicher duerfte speichern:

```text
family_id
reale Kontaktfolge
passive Innenlage
Konfliktspur
Beobachtungsspur
getragene Spur
Reflexionsfrage
passive Reifelesung
Zeit-/Weltbezug
```

Beispiel:

```text
family=dio_0t0v
real_contact_path=negative -> observed -> positive
inner_path=inner_carried -> inner_carried -> inner_carried
reflection_maturity=reflection_reorganized_readable
question=Was hat sich zwischen Konflikt und spaeterem Tragen geaendert?
```

## Nicht erlaubte Inhalte

Der Reflexionsspeicher darf nicht speichern:

```text
Entry erlauben
Entry verbieten
Diese Familie ist sicher
Diese Familie ist immer schlecht
Wenn diese Spur erscheint, dann handeln
Wenn diese Spur erscheint, dann blockieren
```

Er darf keine absolute Form bilden.

Wenn Zahlen oder Beispiele in der Konstruktion stehen, sind sie
Orientierungshilfen. Sie sind keine harten Regeln.

## Unterschied zu Memory

Welt-Memory:

```text
Was ist real passiert?
Welche Form war da?
Welche MCM-Lage war da?
Welche Handlung oder Nicht-Handlung war da?
Welche Konsequenz entstand?
```

Reflexionsspeicher:

```text
Wie wurde diese reale Erfahrung innerlich gelesen?
Wurde Konflikt spaeter getragen?
Blieb eine Spur vorsichtig?
Wurde eine Spur nur beobachtet?
Welche Frage bleibt offen?
```

## Unterschied zu Thought-Memory

Thought-Memory:

```text
Was dachte DIO bei einer realen Lage?
Welche Hypothese entstand?
Wurde der Gedanke spaeter bestaetigt oder widerlegt?
```

Reflexionsspeicher:

```text
Wie liest DIO spaeter seine eigene reale Kontaktgeschichte?
Welche Innenlage blieb stabil?
Welche Spur wurde reorganisiert?
Welche Spur blieb ungelöst?
```

Thought ist eine innere Moeglichkeit.
Reflexion ist ein Rueckblick auf reale Wirkung.

## Reife ohne Gate

Reflexionsreife darf spaeter nur weich wirken.

Sie darf eine innere Frage, Aufmerksamkeit oder Vorsicht verstaerken.
Sie darf aber nicht mechanisch entscheiden.

Zulaessig:

```text
Diese Spur sollte spaeter genauer reflektiert werden.
Diese Spur zeigt Reorganisationspotenzial.
Diese Spur bleibt vorsichtig und ungeloest.
```

Nicht zulaessig:

```text
Diese Spur handelt jetzt.
Diese Spur handelt nie.
Diese Spur bekommt festen Trust.
Diese Spur bekommt festen Block.
```

## Minimaler spaeterer Datensatz

Wenn der Reflexionsspeicher spaeter gebaut wird, sollte der erste Datensatz
klein bleiben:

```text
{
  "family_id": "...",
  "source": "passive_reflection_maturity",
  "real_contact_path": "...",
  "inner_state_path": "...",
  "reflection_maturity": "...",
  "reflection_question": "...",
  "worlds": "...",
  "reward_sum": 0.0,
  "best_reward_sum": 0.0,
  "created_at_run": "...",
  "passive_origin": true
}
```

Keine Rohdatenflut.
Keine vollstaendige Episode.
Keine doppelten Sensorwerte, wenn eine verdichtete Form reicht.

## Speicherwirkung spaeter

Wenn dieser Speicher spaeter aktiv wird, darf er nur als Innenreflexion
angebunden werden:

```text
Memory liefert reale Erfahrung.
Thought liefert gedachte Moeglichkeit.
Reflexionsspeicher liefert Rueckblick auf innere Lesart.
```

Die Handlung darf daraus nicht direkt entstehen.

Handlung darf weiterhin nur aus tragender Kopplung entstehen:

```text
Sehen
Hoeren
Fuehlen
Memory
Realitaetspruefung
Value-Gate
```

## Offene Forschungsfrage

Der naechste aktive Schritt waere nicht sofort Speichern.

Der naechste saubere Schritt waere:

```text
Kann DIO passive Reflexionsreife ueber mehrere kontrollierte Laeufe stabil
wiedererkennen, ohne dass daraus direkt Handlung entsteht?
```

Erst wenn das stabil lesbar ist, darf ein echter Reflexionsspeicher gebaut
werden.

## Passive Schema-Pruefung

Vor einem echten Reflexionsspeicher gibt es eine passive Schema-Pruefung:

```text
DIO_MINI/report_passive_reflection_memory_schema_check.py
```

Diese Pruefung darf nur feststellen:

```text
Dieser passive Reifedatensatz haette spaeter die Mindestinformationen.
Dieser passive Reifedatensatz haette sie nicht.
```

Sie darf nicht speichern.

Sie darf nicht entscheiden.

Sie darf keine Reife erzeugen.

Der aktuelle Probe17/18-Befund:

```text
eligible_passive_schema:
  dio_0t0v
  dio_1vpi
```

Das bedeutet nur:

```text
Beide Spuren tragen genug Kontext fuer einen spaeteren Reflexionsspeicher.
```

Es bedeutet nicht:

```text
Diese Spuren sind aktiv gelernt.
Diese Spuren duerfen handeln.
Diese Spuren bekommen Vertrauen.
```

## Passive Stabilitaetspruefung

Nach der Schema-Pruefung kann eine passive Stabilitaetspruefung mehrere
Schema-Checks vergleichen:

```text
DIO_MINI/report_passive_reflection_schema_stability.py
```

Sie liest:

```text
label_a=schema_check.csv
label_b=schema_check.csv
...
```

Sie prueft passiv:

```text
Bleibt die Schema-Faehigkeit gleich?
Bleibt die Reflexionsreife gleich?
Bleibt die reale Kontaktverdichtung gleich?
Bleibt die Innenzustandsverdichtung gleich?
```

Mit nur einer Quelle wird keine Stabilitaet behauptet. Dann gilt:

```text
single_source_baseline
```

Das bedeutet:

```text
Diese Spur ist die Vergleichsbasis fuer spaetere Laeufe.
```

Es bedeutet nicht:

```text
Diese Spur ist stabil bewiesen.
```

## Erster stabiler Quellenvergleich

Der erste passive Vergleich mit zwei Quellen:

```text
probe17_18
probe18_only
```

zeigt:

```text
dio_0t0v:
  stable_passive_schema
  reflection_reorganized_readable

dio_1vpi:
  stable_passive_schema
  reflection_cautious_unresolved
```

Das ist ein passiver Stabilitaetshinweis.

Es bleibt trotzdem Diagnose:

```text
kein Reflexionsspeicher-Schreiben
kein Trust
kein Schutz
keine Entry-Naehe
keine Motorik
```

## Passive Pipeline

Die passive Reflexionsschema-Kette kann mit einem Runner erzeugt werden:

```text
DIO_MINI/run_passive_reflection_schema_pipeline.py
```

Der Runner buendelt:

```text
Transfer
Konfliktlupe
Innenwahrnehmung
Reflexionskandidaten
Kandidaten-Zeitlinie
Reflexionsreife
Schema-Pruefung
Stabilitaetsvergleich
```

Wichtig:

```text
Der Runner ist kein aktiver Speicherprozess.
Der Runner ist nur Diagnoseautomation.
```

Technische Grenze:

```text
Nullwerte sind gueltige Werte.
0 positive Kontakte bedeutet nicht: Feld fehlt.
0 cautious hits bedeutet nicht: Feld fehlt.
```

Das ist wichtig, weil Reflexionsschema-Daten sonst falsch als unvollstaendig
gelesen werden koennen.

## Wiedererkennung ist nicht automatisch Reflexionsspeicher

Probe19 zeigt einen wichtigen Grenzfall:

```text
Eine Familie kann stabil wiedererkannt werden,
ohne dass daraus ein neuer Reflexionsspeicher entstehen darf.
```

Beispiel:

```text
dio_0arw,dio_0t0v,dio_1u7v:
  inner_carried
  positive reale Kontakte
  ruhige Wiederkehr

dio_14xc:
  inner_open_observation
  beobachtetes Potenzial

dio_00qb,dio_1vpi:
  inner_unfinished
  gehaltene/offene Spur
```

Das ist passiv lesbar, aber nicht automatisch speicherpflichtig.

Ein Reflexionsspeicher braucht eine innere Differenz:

```text
Ich habe etwas wiedererkannt.
Aber es hat sich im Kontakt, in der Innenlage oder in der Konsequenz
so veraendert, dass diese Veraenderung spaeter reflektiv wichtig ist.
```

Damit bleibt der Speicher nicht ueberladen:

```text
nicht jede ruhige Wiederkehr speichern
nicht jede Beobachtung speichern
nicht jede bekannte Familie erneut verdichten

sondern nur:
  relevante Reorganisation
  tragender Konfliktwechsel
  vorsichtig ungelöste Spur
  wiederkehrende Differenz zwischen Kontakt und Innenlage
```

## Passiver Grenzleser

Der Grenzleser fuer diese Entscheidung ist:

```text
DIO_MINI/report_passive_recognition_boundary.py
```

Er liest eine passive Reifungsreflexion und trennt:

```text
stable_recognition_not_memory:
  ruhig wiedererkannt, nicht speicherpflichtig

open_observation_not_memory:
  offen beobachtet, nicht speicherpflichtig

unfinished_trace_not_memory:
  gehalten/unfertig, nicht als Reife speichern

reflection_worthy_difference:
  relevante Differenz, spaeterer Reflexionsspeicher-Kandidat
```

Auch hier gilt:

```text
Die Trennung ist Diagnose.
Sie ist kein Gate und keine Handlungsvorschrift.
```

Validierter Kontrast:

```text
Probe19:
  stabile Wiedererkennung ohne neue Reflexionsspeicher-Reife.

Probe17/18:
  sechs reflexionswuerdige Differenzen.
```

Damit ist die erste notwendige Vorbedingung fuer einen spaeteren
Reflexionsspeicher sichtbar:

```text
DIO muss nicht alles speichern.
DIO darf spaeter nur das speichern, was eine reale Differenz zwischen
Wiedererkennung, Innenlage, Kontaktfolge und Konsequenz traegt.
```
